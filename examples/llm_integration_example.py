"""
Example: LLM Integration with Katrina Agent
Demonstrates how to use external LLMs (OpenAI, Anthropic) or local Ollama models
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agent import Agent


def example_without_llm():
    """Example: Agent without LLM (basic mode)"""
    print("="*60)
    print("🤖 Example 1: Agent without LLM (Basic Mode)")
    print("="*60)
    
    agent = Agent(name="Katrina", memory_dir="./memory_store")
    
    # Test basic calculator
    response = agent.process("calculate 25 + 17", verbose=True)
    print(f"\nFinal Response: {response}\n")


def example_with_ollama():
    """Example: Agent with local Ollama"""
    print("\n" + "="*60)
    print("🦙 Example 2: Agent with Ollama (Local LLM)")
    print("="*60)
    print("Note: This requires Ollama to be installed and running.")
    print("Install from: https://ollama.ai")
    print("Run: ollama pull llama2")
    print("="*60 + "\n")
    
    agent = Agent(
        name="Katrina",
        memory_dir="./memory_store",
        llm_provider="ollama",
        llm_config={
            'ollama_model': 'llama2',
            'ollama_host': 'http://localhost:11434'
        }
    )
    
    # Test with LLM-enhanced reasoning
    response = agent.process("calculate 42 * 13", verbose=True)
    print(f"\nFinal Response: {response}\n")


def example_with_openai():
    """Example: Agent with OpenAI"""
    print("\n" + "="*60)
    print("🧠 Example 3: Agent with OpenAI GPT")
    print("="*60)
    print("Note: This requires an OpenAI API key.")
    print("Set OPENAI_API_KEY environment variable or pass it in config.")
    print("="*60 + "\n")
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_key_here':
        print("⚠️  OpenAI API key not set. Skipping this example.")
        print("Set OPENAI_API_KEY environment variable to run this example.\n")
        return
    
    agent = Agent(
        name="Katrina",
        memory_dir="./memory_store",
        llm_provider="openai",
        llm_config={
            'openai_model': 'gpt-3.5-turbo',
            'openai_api_key': api_key
        }
    )
    
    # Test with OpenAI reasoning
    response = agent.process("calculate 123 + 456", verbose=True)
    print(f"\nFinal Response: {response}\n")


def example_with_anthropic():
    """Example: Agent with Anthropic Claude"""
    print("\n" + "="*60)
    print("🧠 Example 4: Agent with Anthropic Claude")
    print("="*60)
    print("Note: This requires an Anthropic API key.")
    print("Set ANTHROPIC_API_KEY environment variable or pass it in config.")
    print("="*60 + "\n")
    
    # Check if API key is set
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_anthropic_key_here':
        print("⚠️  Anthropic API key not set. Skipping this example.")
        print("Set ANTHROPIC_API_KEY environment variable to run this example.\n")
        return
    
    agent = Agent(
        name="Katrina",
        memory_dir="./memory_store",
        llm_provider="anthropic",
        llm_config={
            'anthropic_model': 'claude-3-sonnet-20240229',
            'anthropic_api_key': api_key
        }
    )
    
    # Test with Anthropic reasoning
    response = agent.process("calculate 789 - 123", verbose=True)
    print(f"\nFinal Response: {response}\n")


def example_switching_providers():
    """Example: Switching between LLM providers at runtime"""
    print("\n" + "="*60)
    print("🔄 Example 5: Switching LLM Providers")
    print("="*60 + "\n")
    
    agent = Agent(
        name="Katrina",
        memory_dir="./memory_store",
        llm_provider="none"
    )
    
    # Check available providers
    if agent.llm_manager:
        available = agent.llm_manager.get_available_providers()
        print(f"Available LLM providers: {available}")
        
        if 'ollama' in available:
            print("\nSwitching to Ollama...")
            agent.llm_manager.switch_provider('ollama')
            response = agent.process("calculate 10 + 20", verbose=False)
            print(f"Response: {response}")
    
    print("\nDisabling LLM...")
    if agent.llm_manager:
        agent.llm_manager.switch_provider('none')
    response = agent.process("calculate 30 + 40", verbose=False)
    print(f"Response: {response}\n")


def main():
    """Run all examples"""
    print("🚀 Katrina Agent - LLM Integration Examples")
    print("This demonstrates integration with external LLMs and local models\n")
    
    # Load environment variables if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded environment variables from .env file\n")
    except ImportError:
        print("ℹ️  python-dotenv not installed. Using system environment variables.\n")
    
    # Run examples
    example_without_llm()
    example_with_ollama()
    example_with_openai()
    example_with_anthropic()
    example_switching_providers()
    
    print("="*60)
    print("✅ Examples completed!")
    print("="*60)
    print("\nNotes:")
    print("- Agent works perfectly without any LLM (basic mode)")
    print("- Ollama provides free local LLM inference")
    print("- OpenAI and Anthropic require API keys")
    print("- LLM enhances reasoning but is not required")


if __name__ == "__main__":
    main()
