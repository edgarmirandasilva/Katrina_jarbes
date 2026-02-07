"""
Base LLM Provider - Abstract interface for all LLM providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    All LLM integrations (OpenAI, Anthropic, Ollama) must implement this interface.
    """
    
    def __init__(self, model_name: str, **kwargs):
        """
        Initialize the LLM provider
        
        Args:
            model_name: Name/identifier of the model to use
            **kwargs: Additional provider-specific parameters
        """
        self.model_name = model_name
        self.config = kwargs
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text completion from the model
        
        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate response in chat format
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{'role': 'user', 'content': 'Hello'}]
            **kwargs: Additional generation parameters
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and properly configured
        
        Returns:
            True if provider can be used, False otherwise
        """
        pass
    
    def get_model_name(self) -> str:
        """Get the current model name"""
        return self.model_name
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return self.config
