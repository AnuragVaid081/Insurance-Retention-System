import json
import logging
import time

import requests

from .config import LLMConfig
from .prompt_builder import PromptBuilder
from .schemas import PolicyContext
from .response_parser import ResponseParser
from .exceptions import (
    LLMConnectionError,
    LLMTimeoutError,
    LLMResponseError
)
from .schemas import ChannelContext

logger = logging.getLogger(__name__)

class LLMService:
    
    def __init__(self):
        
        self.base_url = LLMConfig.BASE_URL
        self.model = LLMConfig.MODEL_NAME

    def analyze_policy(
        self,
        context: PolicyContext
    ) -> str:
        """
        Analyze a policy using the local LLM.
        
        Returns:
            Raw JSON string produced by the model.
        """

        logger.info(
            "Building prompts for the policy %s",
            context.policy_number
        )

        system_prompt, user_prompt = (
            PromptBuilder.buildPrompts(context)
        )

        payload =  self._build_request(
            system_prompt,
            user_prompt
        )


        logger.info("Prompt built successfully")

        response = self._send_request(payload)

        return ResponseParser.parse(
            response["message"]["content"],
            context
        )

        

    def _build_request(
        self,
        system_prompt: str,
        user_prompt: str
    )  -> dict:
        
        return {
            "model": self.model,

            "stream": False,

            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            "options": {
                
                "temperature": LLMConfig.TEMPARTURE,

                "top_p": LLMConfig.TOP_P,

                "num_predict": LLMConfig.NUM_PREDICT
            }
        }
        
    
    def _send_request(
        self,
        payload: dict
    ) -> str:
        """
        Sends the request to the Ollama and returns the JSON string.
        """

        url = f"{self.base_url}/api/chat"

        for attempt in range(LLMConfig.MAX_RETRIES):

            try:

                logger.info(
                    "Sending request to Ollama (Attempt %d/%d)",
                    attempt + 1,
                    LLMConfig.MAX_RETRIES
                )

                response = requests.post(
                    url = url,
                    json = payload,
                    timeout = LLMConfig.TIMEOUT
                )

                response.raise_for_status()

                response_json = response.json()

                if "message" not in response_json:
                    raise LLMResponseError(
                        "Missing 'message' field in Ollama response"
                    )
                
                if "content" not in response_json["message"]:
                    raise LLMResponseError(
                        "Missing 'content' field in Ollama response"
                    )
                
                logger.info("Response recieved succesfully.")

                return response_json
            
            except requests.exceptions.Timeout as e:

                logger.warning(
                    "Ollama request timed out. Retry %d/%d",
                    attempt + 1,
                    LLMConfig.MAX_RETRIES
                )

                if attempt == LLMConfig.MAX_RETRIES - 1:
                
                    raise LLMConnectionError(
                        "Unable to connect to the Ollama server"
                    ) from e
                
            except requests.exceptions.RequestException as e:

                raise  LLMConnectionError(
                    f"HTTP request failed: {e}"
                ) from e
            
            except json.JSONDecodeError as e:

                raise LLMResponseError(
                    "Ollama returned invalid JSON."
                ) from e
            
            time.sleep(LLMConfig.RETRY_DELAY)

        raise LLMConnectionError("Maximum retry attempts exceeded.")
    

    @staticmethod
    def analyze_channel(prompt):

        payload = {
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            url = LLMConfig.BASE_URL,
            json = payload
        )

        response.raise_for_status()

        channel_analysis = json.loads(response.json()["response"])
        
        return channel_analysis
