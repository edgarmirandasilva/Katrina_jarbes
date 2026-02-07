"""
Anthropic Provider - Integration with Anthropic's Claude models
"""

from typing import List, Dict, Optional
from .base_provider import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    """
    Anthropic LLM provider supporting Claude models.
    Requires: pip install anthropic
    """
    
    def __init__(self, model_name: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None, **kwargs):
        """
        Initialize Anthropic provider
        
        Args:
            model_name: Model to use (default: claude-3-sonnet-20240229)
                       Options: claude-3-opus-20240229, claude-3-sonnet-20240229, 
                               claude-3-haiku-20240307, etc.
            api_key: Anthropic API key (if None, will use ANTHROPIC_API_KEY env var)
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        """
        super().__init__(model_name, **kwargs)
        self.api_key = api_key
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            import os
            
            # Use provided API key or fall back to environment variable
            api_key = self.api_key or os.getenv('ANTHROPIC_API_KEY')
            
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                # Still create client, will fail on first request if no key
                self.client = anthropic.Anthropic()
                
        except ImportError:
            print("Warning: anthropic package not installed. Run: pip install anthropic")
            self.client = None
        except Exception as e:
            print(f"Warning: Failed to initialize Anthropic client: {e}")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text completion using Anthropic
        
        Args:
            prompt: Input prompt
            **kwargs: temperature, max_tokens, etc.
            
        Returns:
            Generated text
        """
        if not self.is_available():
            return "Anthropic provider not available. Please install anthropic package and set API key."
        
        try:
            # Convert to chat format
            messages = [{"role": "user", "content": prompt}]
            return self.chat(messages, **kwargs)
            
        except Exception as e:
            return f"Anthropic generation error: {str(e)}"
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat response using Anthropic
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: temperature, max_tokens, etc.
            
        Returns:
            Generated response
        """
        if not self.is_available():
            return "Anthropic provider not available. Please install anthropic package and set API key."
        
        try:
            # Merge default config with provided kwargs
            params = {
                'model': self.model_name,
                'messages': messages,
                'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 500))
            }
            
            response = self.client.messages.create(**params)
            
            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return ""
            
        except Exception as e:
            return f"Anthropic chat error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Anthropic provider is available"""
        return self.client is not None
