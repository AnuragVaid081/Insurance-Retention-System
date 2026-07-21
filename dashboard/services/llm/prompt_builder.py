import json

from pathlib import Path

from .schemas import PolicyContext
from .schemas import Remark


class PromptBuilder:
    """
    Builds prompts for the LLM using prompt templates and the supplied policy context
    """

    PROMPT_DIR = Path("dashboard/services/prompts")


    @staticmethod
    def _format_policy(policy: dict) -> str:
        """
        Convert the policy dictionary into readable JSON String.
        """

        return json.dumps(
            policy,
            indent= 4,
            ensure_ascii=False,
            default=str,
             
        )

    @classmethod
    def _load_prompt(cls, filename: str) -> str:
        """
        Load a prompt template from disk.
        """

        prompt_path = cls.PROMPT_DIR / filename

        with open(prompt_path,"r", encoding = "utf-8") as  file :
            return file.read()
        
    @staticmethod
    def _format_list(items: list[str]) -> str:
        """
        Convert a list into bullet points.
        """
        if not items:
            return "None"
    
        return "\n".join(f"- {item}" for item in items)
    
    @staticmethod
    def _format_remarks(remarks : list[Remark]) -> str:
        """
        Format RM remarks in chronological order
        """
        if not remarks:
            return "No RM remarks available"
        
        remarks = sorted(
            remarks,key= lambda remark: remark.timestamp
        )

        formatted = []

        for remark in remarks:

            formatted.append(
                (
                    f"Date: {remark.timestamp.strftime('%d-%b-%Y %H:%M')}\n"
                    f"Auhtor: {remark.author}\n"
                    f"Remark: {remark.text}"
                )
            )
        
        return "\n\n".join(formatted)
    
    @classmethod
    def buildPrompts(
        cls,
        context: PolicyContext
    ) -> tuple[str,str]:
        """
        Returns:
                (system_prompt, user_prompt)
        """

        system_prompt = cls._load_prompt("system_prompt.txt")

        template = cls._load_prompt(
            "policy_analysis_prompt.txt"
        )

        user_prompt = template.format(

            policy_number = context.policy_number,
            # customer_id = context.customer_id,
            base_probability = f"{context.base_probability:.2f}",
            current_policy = cls._format_policy(context.current_policy),
            historical_insights = cls._format_list(context.historical_insights),
            remarks = cls._format_remarks(context.remarks)
        )
        return system_prompt, user_prompt