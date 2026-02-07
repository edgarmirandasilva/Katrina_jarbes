"""
LLM Manager - Manages multiple LLM providers and selects the appropriate one
"""

from typing import Optional, Dict, Any, List
from .base_provider import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .ollama_provider import OllamaProvider


class LLMManager:
    """
    Manages multiple LLM providers and provides a unified interface.
    Automatically falls back to local/offline mode if external APIs unavailable.
    """
    
    def __init__(self, 
                 preferred_provider: str = "ollama",
                 openai_api_key: Optional[str] = None,
                 anthropic_api_key: Optional[str] = None,
                 ollama_host: str = "http://localhost:11434",
                 **kwargs):
        """
        Initialize LLM Manager
        
        Args:
            preferred_provider: Preferred provider to use ('openai', 'anthropic', 'ollama', or 'none')
                              Default: 'ollama' (local, no API key needed)
            openai_api_key: OpenAI API key (optional)
            anthropic_api_key: Anthropic API key (optional)
            ollama_host: Ollama server URL (default: http://localhost:11434)
            **kwargs: Additional provider-specific config
        """
        self.preferred_provider = preferred_provider.lower()
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.config = kwargs
        
        # Initialize providers based on preference
        if preferred_provider.lower() != 'none':
            self._initialize_providers(openai_api_key, anthropic_api_key, ollama_host)
        
        self.current_provider = self._select_provider()
    
    def _initialize_providers(self, openai_key, anthropic_key, ollama_host):
        """Initialize available LLM providers"""
        
        # Initialize OpenAI if key provided or in config
        if openai_key or self.config.get('openai_model'):
            try:
                model = self.config.get('openai_model', 'gpt-3.5-turbo')
                self.providers['openai'] = OpenAIProvider(
                    model_name=model,
                    api_key=openai_key,
                    **self.config.get('openai_config', {})
                )
            except Exception as e:
                print(f"Failed to initialize OpenAI provider: {e}")
        
        # Initialize Anthropic if key provided or in config
        if anthropic_key or self.config.get('anthropic_model'):
            try:
                model = self.config.get('anthropic_model', 'claude-3-sonnet-20240229')
                self.providers['anthropic'] = AnthropicProvider(
                    model_name=model,
                    api_key=anthropic_key,
                    **self.config.get('anthropic_config', {})
                )
            except Exception as e:
                print(f"Failed to initialize Anthropic provider: {e}")
        
        # Always try to initialize Ollama (local, no API key needed)
        try:
            model = self.config.get('ollama_model', 'llama2')
            self.providers['ollama'] = OllamaProvider(
                model_name=model,
                host=ollama_host,
                **self.config.get('ollama_config', {})
            )
        except Exception as e:
            print(f"Failed to initialize Ollama provider: {e}")
    
    def _select_provider(self) -> Optional[BaseLLMProvider]:
        """Select the best available provider"""
        
        # If no LLM mode (agent works without LLM)
        if self.preferred_provider == 'none':
            return None
        
        # Try preferred provider first
        if self.preferred_provider in self.providers:
            provider = self.providers[self.preferred_provider]
            if provider.is_available():
                print(f"Using {self.preferred_provider} provider: {provider.get_model_name()}")
                return provider
        
        # Fallback: try providers in order of preference
        fallback_order = ['ollama', 'openai', 'anthropic']
        for name in fallback_order:
            if name in self.providers and self.providers[name].is_available():
                print(f"Falling back to {name} provider: {self.providers[name].get_model_name()}")
                return self.providers[name]
        
        print("Warning: No LLM providers available. Agent will work in basic mode.")
        return None
    
    def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate text using the current provider
        
        Args:
            prompt: Input prompt
            **kwargs: Generation parameters
            
        Returns:
            Generated text or None if no provider available
        """
        if self.current_provider is None:
            return None
        
        return self.current_provider.generate(prompt, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """
        Generate chat response using the current provider
        
        Args:
            messages: Chat messages
            **kwargs: Generation parameters
            
        Returns:
            Generated response or None if no provider available
        """
        if self.current_provider is None:
            return None
        
        return self.current_provider.chat(messages, **kwargs)
    
    def is_enabled(self) -> bool:
        """Check if LLM is enabled and available"""
        return self.current_provider is not None
    
    def get_current_provider_name(self) -> str:
        """Get name of current provider"""
        if self.current_provider is None:
            return "none"
        
        for name, provider in self.providers.items():
            if provider == self.current_provider:
                return name
        return "unknown"
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def switch_provider(self, provider_name: str) -> bool:
        """
        Switch to a different provider
        
        Args:
            provider_name: Name of provider to switch to
            
        Returns:
            True if switch successful, False otherwise
        """
        provider_name = provider_name.lower()
        
        if provider_name == 'none':
            self.current_provider = None
            print("LLM disabled - agent will work in basic mode")
            return True
        
        if provider_name in self.providers and self.providers[provider_name].is_available():
            self.current_provider = self.providers[provider_name]
            print(f"Switched to {provider_name} provider: {self.current_provider.get_model_name()}")
            return True
        
        print(f"Provider {provider_name} not available")
        return False
