"""
Configuration for the local LLM (Ollama Qwen2.5:7b)
This file will contain the model/server specific settings.
"""

from dataclasses import dataclass

@dataclass(frozen= True)
class LLMConfig:

    # Ollama server
    BASE_URL: str = "http://localhost:11434"

    # Local Model
    MODEL_NAME: str = "qwen2.5:7b"

    # Generation Settings
    TEMPARTURE: float = 0.1
    TOP_P: float = 0.9
    NUM_PREDICT: int = 700

    # Timeout settings
    TIMEOUT:int = 120

    # Probability Adjustment Limits
    MIN_ADJUSTMENT :int = -15
    MAX_ADJUSTMENT :int = 15

    # Retry settings
    MAX_RETRIES :int = 3
    RETRY_DELAY :int = 2

config = LLMConfig( )