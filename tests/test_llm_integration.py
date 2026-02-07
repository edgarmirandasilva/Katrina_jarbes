"""
Tests for LLM Integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm import BaseLLMProvider, OpenAIProvider, AnthropicProvider, OllamaProvider, LLMManager


def test_base_provider_interface():
    """Test that providers implement the base interface"""
    print("Testing base provider interface...")
    
    # Test that all providers have required methods
    providers = [OpenAIProvider, AnthropicProvider, OllamaProvider]
    
    for ProviderClass in providers:
        provider = ProviderClass(model_name="test-model")
        
        # Check required methods exist
        assert hasattr(provider, 'generate'), f"{ProviderClass.__name__} missing generate method"
        assert hasattr(provider, 'chat'), f"{ProviderClass.__name__} missing chat method"
        assert hasattr(provider, 'is_available'), f"{ProviderClass.__name__} missing is_available method"
        assert hasattr(provider, 'get_model_name'), f"{ProviderClass.__name__} missing get_model_name method"
        
        # Test get_model_name
        assert provider.get_model_name() == "test-model"
    
    print("✅ Base provider interface tests passed")


def test_llm_manager_initialization():
    """Test LLM Manager initialization"""
    print("Testing LLM Manager initialization...")
    
    # Test with 'none' provider (should not initialize any providers)
    manager = LLMManager(preferred_provider='none')
    assert not manager.is_enabled()
    assert manager.get_current_provider_name() == 'none'
    
    # Test with ollama provider (may or may not be available)
    manager = LLMManager(preferred_provider='ollama')
    # Just check it doesn't crash
    available = manager.get_available_providers()
    assert isinstance(available, list)
    
    print("✅ LLM Manager initialization tests passed")


def test_llm_manager_fallback():
    """Test that LLM Manager falls back gracefully"""
    print("Testing LLM Manager fallback...")
    
    # Request a provider that likely doesn't have credentials
    manager = LLMManager(preferred_provider='openai')
    
    # Should either use openai if available, or fallback
    # In either case, shouldn't crash
    provider_name = manager.get_current_provider_name()
    assert provider_name in ['openai', 'anthropic', 'ollama', 'none']
    
    print("✅ LLM Manager fallback tests passed")


def test_llm_manager_switching():
    """Test switching between providers"""
    print("Testing LLM Manager provider switching...")
    
    manager = LLMManager(preferred_provider='none')
    
    # Test switching to none
    result = manager.switch_provider('none')
    assert result is True
    assert manager.get_current_provider_name() == 'none'
    
    # Test switching to non-existent provider
    result = manager.switch_provider('nonexistent')
    assert result is False
    
    print("✅ LLM Manager switching tests passed")


def test_openai_provider_without_key():
    """Test OpenAI provider without API key"""
    print("Testing OpenAI provider without key...")
    
    # Create provider without key (should handle gracefully)
    provider = OpenAIProvider(model_name="gpt-3.5-turbo", api_key="invalid")
    
    # Provider should exist but may not be available
    assert provider.get_model_name() == "gpt-3.5-turbo"
    
    # Attempting to generate should return error message, not crash
    result = provider.generate("test prompt")
    assert isinstance(result, str)
    
    print("✅ OpenAI provider without key tests passed")


def test_anthropic_provider_without_key():
    """Test Anthropic provider without API key"""
    print("Testing Anthropic provider without key...")
    
    # Create provider without key (should handle gracefully)
    provider = AnthropicProvider(model_name="claude-3-sonnet-20240229", api_key="invalid")
    
    # Provider should exist but may not be available
    assert provider.get_model_name() == "claude-3-sonnet-20240229"
    
    # Attempting to generate should return error message, not crash
    result = provider.generate("test prompt")
    assert isinstance(result, str)
    
    print("✅ Anthropic provider without key tests passed")


def test_ollama_provider_basic():
    """Test Ollama provider basic functionality"""
    print("Testing Ollama provider...")
    
    # Create provider
    provider = OllamaProvider(model_name="llama2")
    
    # Provider should exist
    assert provider.get_model_name() == "llama2"
    
    # Check availability (depends on if Ollama is running)
    is_available = provider.is_available()
    
    if is_available:
        print("  Ollama is available, testing generation...")
        result = provider.generate("Say hello")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"  Generated: {result[:50]}...")
    else:
        print("  Ollama not available (expected if not installed/running)")
    
    print("✅ Ollama provider tests passed")


def test_agent_with_llm():
    """Test Agent with LLM integration"""
    print("Testing Agent with LLM integration...")
    
    from src.agent import Agent
    
    # Test agent with no LLM (basic mode)
    agent = Agent(name="TestAgent", memory_dir="./test_memory", llm_provider="none")
    assert agent.llm_manager is None
    
    response = agent.process("calculate 5 + 3", verbose=False)
    assert "8" in response
    
    # Test agent with ollama (may or may not be available)
    agent = Agent(
        name="TestAgent",
        memory_dir="./test_memory",
        llm_provider="ollama",
        llm_config={'ollama_model': 'llama2'}
    )
    
    # Agent should work even if Ollama not available
    response = agent.process("calculate 10 + 20", verbose=False)
    assert "30" in response
    
    print("✅ Agent with LLM integration tests passed")


def test_reasoning_engine_with_llm():
    """Test ReasoningEngine with LLM"""
    print("Testing ReasoningEngine with LLM...")
    
    from src.agent import ReasoningEngine
    
    # Test without LLM
    reasoning = ReasoningEngine(llm_manager=None)
    thought = reasoning.think("Test observation")
    assert isinstance(thought, str)
    assert "Test observation" in thought
    
    reflection = reasoning.reflect({'success': True, 'result': 'test'})
    assert isinstance(reflection, str)
    
    # Test with LLM manager (but no actual LLM available)
    manager = LLMManager(preferred_provider='none')
    reasoning = ReasoningEngine(llm_manager=manager)
    
    thought = reasoning.think("Test observation 2")
    assert isinstance(thought, str)
    
    print("✅ ReasoningEngine with LLM tests passed")


def run_all_tests():
    """Run all LLM integration tests"""
    print("="*60)
    print("Running LLM Integration Tests")
    print("="*60)
    
    try:
        test_base_provider_interface()
        test_llm_manager_initialization()
        test_llm_manager_fallback()
        test_llm_manager_switching()
        test_openai_provider_without_key()
        test_anthropic_provider_without_key()
        test_ollama_provider_basic()
        test_reasoning_engine_with_llm()
        test_agent_with_llm()
        
        print("\n" + "="*60)
        print("✅ ALL LLM INTEGRATION TESTS PASSED!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
