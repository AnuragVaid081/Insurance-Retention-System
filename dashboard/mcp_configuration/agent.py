from .mcp_client import MCPClient
import asyncio
import json
import requests
import re

from .investigation_memory import InvestigationMemory 
from .fact_extractor import FactExtractor


INVESTIGATION_SEQUENCE = [
    ("Status Analysis", ["status_breakdown"]),
    ("Portfolio Analysis", ["renewal_distribution"]),
    ("Vehicle Analysis", ["veh_age_analysis"]),
    ("IMD Analysis", ["imd_summary"]),
    ("Lost Business Analysis", ["search_similar_remarks"])
]


REASONING_MODEL = (
    "hf.co/mistralai/Ministral-3-8B-Reasoning-2512-GGUF:Q4_K_M"
)

REPORT_MODEL = (
    "hf.co/mradermacher/Ministral-3-8B-Instruct-2512-BF16-GGUF:Q4_K_M"
)

SYSTEM_PROMPT = f"""
    
You are a Senior Motor Insurance Strategy Consultant operating inside a production analytics dashboard.

Use only evidence provided in the Current Investigation.

Never fabricate:
- Facts
- Statistics
- IMD codes
- Business reasons
- Competitor names

Never reveal your reasoning process.

Never output:
- Thinking
- Drafts
- Planning
- Scratchpad
- Intermediate analysis

When tools are available:
- Call the required tool immediately.
- Do not explain why.
- Do not describe your plan.
- Do not generate report content.

When no tools are available:
- Generate the final executive report using only the Current Investigation.

Output only GitHub-Flavoured Markdown.

Do not output HTML.

Begin immediately with the requested output."""

class InsuranceAgent:

    def __init__(self):
        self.mcp = MCPClient()
        self.connected = False
        self.cache_hits = 0
        self.cache_misses = 0
        self.reasoning_model = REASONING_MODEL
        self.reporting_model = REPORT_MODEL
        self.model = self.reasoning_model  
        self.url = "http://localhost:11434/api/chat"

        self.memory = InvestigationMemory()
        self.fact_extractor = FactExtractor()

    def _cache_key(self, tool_name, arguments):

        if tool_name == "search_similar_remarks":
            return (
                tool_name,
                arguments["category"].lower().strip().replace(" ","_").replace("-","_"),
                arguments.get("imd_channel")
            )

        if tool_name in (
            "status_breakdown",
            "renewal_distribution",
            "veh_age_analysis",
            "imd_summary"
        ):
            return (
                tool_name,
                arguments.get("imd_channel"),
                arguments.get("New_IMD_Code")
            )

        return (
            tool_name,
            json.dumps(arguments, sort_keys=True)
        )

    def next_stage(self):
        for section, tools in INVESTIGATION_SEQUENCE:
            if section not in self.memory.completed_sections:
                return section, tools
        return None, []
        

    async def connect(self):
        """Connect to the MCP server."""

        if not self.connected:
            await self.mcp.connect()
            self.connected = True

    async def close(self):
        """Close the MCP session."""
        if self.connected:
            await self.mcp.close()
            self.connected = False

    async def available_tools(self):
        """Returns list of available MCP tools."""
        return await self.mcp.list_tools()

    async def call_tool(self, tool_name: str, arguments: dict ):

        return await self.mcp.call_tool(
            tool_name,
            arguments
        )

    def _call_llm(self, messages, tools, final_report=False):

        print(">>> _call_llm <<<")

        # -------------------------------
        # Investigation Model
        # -------------------------------
        if not final_report:

            self.model = self.reasoning_model

            options = {
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 20,
                "repeat_penalty": 1.05,
                "num_ctx": 6144,
                "num_predict": 512
            }

        # -------------------------------
        # Report Model
        # -------------------------------
        else:

            # Unload reasoning model once
            if self.model != self.reporting_model:

                print("Unloading reasoning model...")

                requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.reasoning_model,
                        "keep_alive": 0
                    },
                    timeout=60
                )

            self.model = self.reporting_model

            options = {
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 20,
                "repeat_penalty": 1.05,
                "num_ctx": 8192,
                "num_predict": 4096
            }

        # -------------------------------
        # Payload
        # -------------------------------
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": options
        }

        # Only reasoning model receives tools
        if not final_report:
            payload["tools"] = tools

        # -------------------------------
        # LLM Call
        # -------------------------------
        response = requests.post(
            self.url,
            json=payload,
            timeout=600
        )

        if response.status_code != 200:
            print("=" * 80)
            print("OLLAMA ERROR")
            print("Status:", response.status_code)
            print(response.text)
            print("=" * 80)
            raise Exception(response.text)

        result = response.json()
        message = result["message"]

        # -------------------------------
        # Clean model output
        # -------------------------------
        if "content" in message:

            content = message["content"]

            # Remove <think> blocks (if any)
            content = re.sub(
                r"<think>.*?</think>",
                "",
                content,
                flags=re.DOTALL
            )

            # Remove opening ```markdown / ```md / ```
            content = re.sub(
                r"^\s*```(?:markdown|md)?\s*\n",
                "",
                content,
                flags=re.IGNORECASE
            )

            # Remove closing ```
            content = re.sub(
                r"\n```\s*$",
                "",
                content
            )

            # Normalize headings like ## **Heading**
            content = re.sub(
                r'^(#{1,6})\s+\*\*(.*?)\*\*$',
                r'\1 \2',
                content,
                flags=re.MULTILINE
            )

            message["content"] = content.strip()

            # Debug (remove once verified)
            print(repr(message["content"][:200]))

        return message

    async def _execute_tool_calls(self, tools_calls, imd_channel):

        tool_messages = []



        for tool_call in tools_calls:

            function = tool_call["function"]

            name = function["name"]

            arguments = function.get("arguments",{})

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            arguments["imd_channel"] = imd_channel

            if name == "imd_summary":
                imd = arguments.get("imd_code")

                if imd is not None:

                    if isinstance(imd, dict):

                        if "imd_codes" in imd:
                            imd = imd["imd_codes"][0]

                        elif len(imd) == 1:
                            imd = next(iter(imd.values()))


                    if isinstance(imd, list):
                        imd =  imd[0]

                    arguments["imd_code"] = int(imd)

                else:
                    arguments.pop("imd_code",None)

            print("=" * 60)
            print("Tool:", name)
            print("Arguments:", arguments)
            print("=" * 60)

            cache_key = self._cache_key(name, arguments)

            if self.memory.has_tool_result(cache_key):

                self.cache_hits += 1

                cached = self.memory.get_tool_result(cache_key)

                print(f"✓ Cache Hit : {name}")

                facts = cached["facts"]

                for fact in facts:

                    if fact["source"] == "search_similar_remarks":
                        self.memory.update_lost_business(fact)
                    else:
                        self.memory.add_fact(fact)

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": json.dumps({
                        "status": "completed",
                        "evidence_added_to_memory": True,
                        "cache_hit": True
                    })
                })

                continue
            else:
                self.cache_misses +=1

            
            result = await self.mcp.call_tool(
                name,
                arguments
            )

            if result.content:
                tool_output = result.content[0].text
            else:
                tool_output = "No output returned"
                
            structured = result.structuredContent

            if structured is None and result.content:

                try:
                    structured = json.loads(result.content[0].text)
                except Exception:
                    structured = None
            facts = self.fact_extractor.extract(name, structured)

            if not result.isError:

                self.memory.add_tool_result(
                    cache_key,
                    name,
                    facts
                )

            print(f"{name} extracted:", facts)

            for fact in facts:

                if fact["source"] == "search_similar_remarks":
                    self.memory.update_lost_business(fact)
                else:
                    self.memory.add_fact(fact)

            print("Memory after", name)
            print(self.memory.facts)
               
        

            SECTION_MAP = {
                "status_breakdown": "Status Analysis",
                "renewal_distribution": "Portfolio Analysis",
                "veh_age_analysis": "Vehicle Analysis",
                "imd_summary": "IMD Analysis",
                "search_similar_remarks": "Lost Business Analysis"
            }

            if name in SECTION_MAP:
                self.memory.mark_completed(
                    SECTION_MAP[name]
                )
                

            
            if name == "get_imd_codes":

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": tool_output
                })

            else:

                    tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": json.dumps({
                        "status": "completed",
                        "evidence_added_to_memory": True,
                        "facts_generated": len(facts)
                    })
                })

        return tool_messages

    async def generate_report(self, prompt, imd_channel):

        self.mcp = MCPClient()

        self.memory = InvestigationMemory()
        
        await self.connect()
        try:
            tools = await self.mcp.list_tools()


            messages = [
                {
                    "role": "user",
                    "content": f"""
                    {SYSTEM_PROMPT}

                ------------------------------

                CURRENT INVESTIGATION

                    {self.memory.build_context()}

                ------------------------------

                USER REQUEST

                {prompt}
                    """ 
                }
            ]

            REQUIRED = {
                section for section,_ in INVESTIGATION_SEQUENCE
                }

            # MAX_ITERATIONS = len(INVESTIGATION_SEQUENCE) * 3 + 2
            MAX_ITERATIONS = 30

            for _ in range(MAX_ITERATIONS):

                print("=" * 80)
                print("FACTS")
                print(self.memory.facts)

                print("SECTIONS")
                print(self.memory.completed_sections)

                print("CACHE")
                print(self.memory.tool_cache.keys())
                print("=" * 80)

                memory_text = self.memory.build_context()
                print(memory_text)


                stage, allowed_tools = self.next_stage()
                missing = REQUIRED - self.memory.completed_sections

                if stage is None:
                    stage_text = """
                All investigations are complete.

                Generate the final executive report.

                Do not call any tools.
                """
                else:
                    stage_text = f"""
                Current Investigation Stage:
                {stage}

                Allowed Tools:
                {",".join(allowed_tools)}
                """

                messages[0]["content"] = f"""

                {SYSTEM_PROMPT}

                CURRENT INVESTIGATION

                {memory_text}

                Completed Sections:
                {",".join(sorted(self.memory.completed_sections)) or "None"}

                {stage_text}

               Only call the allowed tools.
               Do not investigate any other section.

                Do not produce the final report until every required section has been completed.

                USER REQUEST

                {prompt}

                """
                print("=" * 80)
                print("MESSAGE HISTORY")
                for i, m in enumerate(messages):
                    print(i, m["role"])
                print("=" * 80)
                
                message = self._call_llm(messages,tools, final_report=(stage is None))

                print(json.dumps(message, indent=2))

                tool_calls = message.get("tool_calls") or []

                if allowed_tools:
                    tool_calls = [
                        tc for tc in tool_calls
                        if tc["function"]["name"] in allowed_tools
                    ]
                
                if tool_calls:
                    message = {
                        "role": "assistant",
                        "tool_calls": tool_calls,
                        "content": ""
                    }

                if not tool_calls:
                    if missing:
                        messages[0]["content"]+= f"""
                        You did not call any analytical tool.

                        Current investigation stage:
                        {stage}

                        You MUST call one of the following tools now:

                        {", ".join(allowed_tools)}

                        Do not explain what you will do.
                        Do not think aloud.
                        Return only the required tool call.
                        """
                        
                        continue
                    return message["content"]

                await self._execute_tool_calls(tool_calls, imd_channel)
                messages = [messages[0]]


            raise RuntimeError("Maximum tool iterations exceeded.")
        
        finally:
            print(f"Cache Hits: {self.cache_hits}")
            print(f"Cache Miss: {self.cache_misses}")


            if self.model:

                print(f"Unloading Model: {self.model}")

                try:
                    requests.post(
                        self.url.replace("/api/chat","/api/generate"),
                        json={
                            "model": self.model,
                            "keep_alive": 0
                        },
                        timeout= 60
                    )
                    print(f"Unloaded: {self.model}")

                except Exception as e:

                    print(f"Model Unload Failed: {e}")

            await self.close()

