"""
LLM Integration Module

Provides integration with external LLMs (OpenAI, Anthropic) and local models (Ollama)
"""

from .base_provider import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .ollama_provider import OllamaProvider
from .llm_manager import LLMManager

__all__ = [
    'BaseLLMProvider',
    'OpenAIProvider',
    'AnthropicProvider',
    'OllamaProvider',
    'LLMManager'
]
