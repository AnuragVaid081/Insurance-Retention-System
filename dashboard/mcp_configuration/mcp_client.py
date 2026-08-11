import copy
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path
from contextlib import AsyncExitStack

SERVER_PATH = Path(__file__).parent / "server.py"

class MCPClient:

    def __init__(self):
        self.session = None

    async def connect(self):
        """
        Starts the MCP session and establishes a session.
        """
        self.exit_stack = AsyncExitStack()

        server_params = StdioServerParameters(
            command = "python",
            args=[str(SERVER_PATH)],
            env = None
        )

        transport = await self.exit_stack.enter_async_context(stdio_client(server_params))

        self.read, self.write = transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(
            self.read,
            self.write
            )
        )

        await self.session.initialize()

    async def list_tools(self):
        result = await self.session.list_tools()

        ollama_tools = []

        for tool in result.tools:

            schema = copy.deepcopy(tool.inputSchema)

            # Hide imd_channel from the LLM 
            print("schema type:", type(schema))
            print("schema:", schema)
            schema["properties"].pop("imd_channel", None)
            if "imd_channel" in schema.get("required",[]):
                schema["required"].remove("imd_channel")

            ollama_tools.append({
                "type": "function",
                "function":{
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": schema
                },
            })

        return ollama_tools

    async def close(self):

        if self.exit_stack:
            await self.exit_stack.aclose()

        self.exit_stack = None
        self.session = None
        self.read = None
        self.write = None



    async def call_tool(self, name: str, arguments: dict):
        result = await self.session.call_tool(name, arguments)
        return result

if main := __name__ == "__main__":
    import asyncio

    async def main_async():
        client = MCPClient()
        await client.connect()

        tools = await client.list_tools()
        print("Tools:", tools)

        await client.close()

    asyncio.run(main_async())



           

