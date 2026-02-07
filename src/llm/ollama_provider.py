"""
Ollama Provider - Integration with local Ollama models
"""

from typing import List, Dict, Optional
from .base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """
    Ollama LLM provider for local models.
    Requires: Ollama installed and running locally (https://ollama.ai)
    Optional: pip install ollama (for Python client)
    """
    
    def __init__(self, model_name: str = "llama2", host: str = "http://localhost:11434", **kwargs):
        """
        Initialize Ollama provider
        
        Args:
            model_name: Model to use (default: llama2)
                       Options: llama2, mistral, codellama, phi, etc.
                       Run 'ollama list' to see available models
            host: Ollama server URL (default: http://localhost:11434)
            **kwargs: Additional parameters (temperature, num_predict, etc.)
        """
        super().__init__(model_name, **kwargs)
        self.host = host
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Ollama client"""
        try:
            # Try to use official ollama Python package
            import ollama
            self.client = ollama.Client(host=self.host)
            self.use_package = True
        except ImportError:
            # Fall back to direct HTTP requests
            try:
                import requests
                self.client = requests
                self.use_package = False
            except ImportError:
                print("Warning: Neither ollama nor requests package installed.")
                print("Install with: pip install ollama  OR  pip install requests")
                self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text completion using Ollama
        
        Args:
            prompt: Input prompt
            **kwargs: temperature, num_predict (max tokens), etc.
            
        Returns:
            Generated text
        """
        if not self.is_available():
            return "Ollama provider not available. Please install Ollama and ensure it's running."
        
        try:
            if self.use_package:
                # Use ollama package
                response = self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    options={
                        'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        'num_predict': kwargs.get('num_predict', self.config.get('num_predict', 500))
                    }
                )
                return response['response']
            else:
                # Use direct HTTP request
                url = f"{self.host}/api/generate"
                payload = {
                    'model': self.model_name,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        'num_predict': kwargs.get('num_predict', self.config.get('num_predict', 500))
                    }
                }
                
                response = self.client.post(url, json=payload, timeout=60)
                response.raise_for_status()
                return response.json()['response']
                
        except Exception as e:
            return f"Ollama generation error: {str(e)}. Make sure Ollama is running."
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat response using Ollama
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: temperature, num_predict, etc.
            
        Returns:
            Generated response
        """
        if not self.is_available():
            return "Ollama provider not available. Please install Ollama and ensure it's running."
        
        try:
            if self.use_package:
                # Use ollama package
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    options={
                        'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        'num_predict': kwargs.get('num_predict', self.config.get('num_predict', 500))
                    }
                )
                return response['message']['content']
            else:
                # Use direct HTTP request
                url = f"{self.host}/api/chat"
                payload = {
                    'model': self.model_name,
                    'messages': messages,
                    'stream': False,
                    'options': {
                        'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        'num_predict': kwargs.get('num_predict', self.config.get('num_predict', 500))
                    }
                }
                
                response = self.client.post(url, json=payload, timeout=60)
                response.raise_for_status()
                return response.json()['message']['content']
                
        except Exception as e:
            return f"Ollama chat error: {str(e)}. Make sure Ollama is running."
    
    def is_available(self) -> bool:
        """Check if Ollama provider is available"""
        if self.client is None:
            return False
        
        try:
            # Test connection to Ollama server
            if self.use_package:
                self.client.list()
                return True
            else:
                url = f"{self.host}/api/tags"
                response = self.client.get(url, timeout=5)
                return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> List[str]:
        """
        List available models in Ollama
        
        Returns:
            List of model names
        """
        if not self.is_available():
            return []
        
        try:
            if self.use_package:
                models = self.client.list()
                return [m['name'] for m in models.get('models', [])]
            else:
                url = f"{self.host}/api/tags"
                response = self.client.get(url, timeout=5)
                response.raise_for_status()
                return [m['name'] for m in response.json().get('models', [])]
        except Exception:
            return []
