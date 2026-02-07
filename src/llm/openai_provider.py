"""
OpenAI Provider - Integration with OpenAI's GPT models
"""

from typing import List, Dict, Optional
from .base_provider import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI LLM provider supporting GPT models.
    Requires: pip install openai
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider
        
        Args:
            model_name: Model to use (default: gpt-3.5-turbo)
                       Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        """
        super().__init__(model_name, **kwargs)
        self.api_key = api_key
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            import openai
            import os
            
            # Use provided API key or fall back to environment variable
            api_key = self.api_key or os.getenv('OPENAI_API_KEY')
            
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                # Still create client, will fail on first request if no key
                self.client = openai.OpenAI()
                
        except ImportError:
            print("Warning: openai package not installed. Run: pip install openai")
            self.client = None
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text completion using OpenAI
        
        Args:
            prompt: Input prompt
            **kwargs: temperature, max_tokens, etc.
            
        Returns:
            Generated text
        """
        if not self.is_available():
            return "OpenAI provider not available. Please install openai package and set API key."
        
        try:
            # Convert to chat format (OpenAI's preferred method)
            messages = [{"role": "user", "content": prompt}]
            return self.chat(messages, **kwargs)
            
        except Exception as e:
            return f"OpenAI generation error: {str(e)}"
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat response using OpenAI
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: temperature, max_tokens, etc.
            
        Returns:
            Generated response
        """
        if not self.is_available():
            return "OpenAI provider not available. Please install openai package and set API key."
        
        try:
            # Merge default config with provided kwargs
            params = {
                'model': self.model_name,
                'messages': messages,
                'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 500))
            }
            
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI chat error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if OpenAI provider is available"""
        return self.client is not None
