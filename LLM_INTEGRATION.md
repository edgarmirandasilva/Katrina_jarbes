# LLM Integration Guide

## Overview

Katrina Agent now supports integration with external Large Language Models (LLMs) to enhance reasoning capabilities. The integration is completely optional - the agent works perfectly without any LLM in basic mode.

## Supported LLM Providers

### 1. **Ollama** (Local, Free) ⭐ Recommended
- **Description**: Run LLMs locally on your machine
- **Cost**: Free
- **Privacy**: Complete - all processing happens locally
- **Requirements**: 
  - Install Ollama from https://ollama.ai
  - Pull models: `ollama pull llama2`
- **Models**: llama2, mistral, codellama, phi, and many more

### 2. **OpenAI** (Cloud, Paid)
- **Description**: GPT models from OpenAI
- **Cost**: Pay per API call
- **Requirements**: 
  - OpenAI API key
  - `pip install openai`
- **Models**: gpt-3.5-turbo, gpt-4, gpt-4-turbo

### 3. **Anthropic** (Cloud, Paid)
- **Description**: Claude models from Anthropic
- **Cost**: Pay per API call
- **Requirements**: 
  - Anthropic API key
  - `pip install anthropic`
- **Models**: claude-3-opus, claude-3-sonnet, claude-3-haiku

## Installation

### Basic Installation (No LLM)
```bash
# Agent works out-of-the-box with no dependencies
python examples/basic_example.py
```

### With Ollama (Local LLM)
```bash
# 1. Install Ollama
# Visit https://ollama.ai and follow installation instructions

# 2. Pull a model
ollama pull llama2

# 3. Run Ollama (usually auto-starts as service)
ollama serve

# 4. Install Python client (optional, will use HTTP fallback if not installed)
pip install ollama

# 5. Use with agent
python examples/llm_integration_example.py
```

### With OpenAI
```bash
# 1. Install OpenAI package
pip install openai

# 2. Set API key
export OPENAI_API_KEY="your-key-here"

# 3. Use with agent
python examples/llm_integration_example.py
```

### With Anthropic
```bash
# 1. Install Anthropic package
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY="your-key-here"

# 3. Use with agent
python examples/llm_integration_example.py
```

## Usage Examples

### Example 1: Basic Agent (No LLM)
```python
from src.agent import Agent

# Agent works without any LLM
agent = Agent(name="Katrina", memory_dir="./memory_store")

response = agent.process("calculate 5 + 3")
print(response)  # "The result of 5 + 3 is 8"
```

### Example 2: Agent with Ollama
```python
from src.agent import Agent

# Use local Ollama for enhanced reasoning
agent = Agent(
    name="Katrina",
    llm_provider="ollama",
    llm_config={
        'ollama_model': 'llama2',
        'ollama_host': 'http://localhost:11434'
    }
)

response = agent.process("calculate 42 * 13")
# Now includes LLM-enhanced reasoning in the thinking process
```

### Example 3: Agent with OpenAI
```python
from src.agent import Agent
import os

agent = Agent(
    name="Katrina",
    llm_provider="openai",
    llm_config={
        'openai_model': 'gpt-3.5-turbo',
        'openai_api_key': os.getenv('OPENAI_API_KEY')
    }
)

response = agent.process("calculate 123 + 456")
```

### Example 4: Agent with Anthropic Claude
```python
from src.agent import Agent
import os

agent = Agent(
    name="Katrina",
    llm_provider="anthropic",
    llm_config={
        'anthropic_model': 'claude-3-sonnet-20240229',
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY')
    }
)

response = agent.process("calculate 789 - 123")
```

### Example 5: Using Environment Variables
```python
from src.agent import Agent
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

agent = Agent(
    name="Katrina",
    llm_provider="openai",  # Will use OPENAI_API_KEY from .env
    llm_config={
        'openai_model': 'gpt-3.5-turbo'
    }
)
```

### Example 6: Switching Providers at Runtime
```python
from src.agent import Agent

agent = Agent(name="Katrina", llm_provider="ollama")

# Check available providers
available = agent.llm_manager.get_available_providers()
print(f"Available: {available}")

# Switch to different provider
agent.llm_manager.switch_provider('openai')

# Disable LLM
agent.llm_manager.switch_provider('none')
```

## Configuration

### Environment Variables (.env file)
```bash
# LLM Provider Selection
LLM_PROVIDER=ollama  # Options: 'none', 'openai', 'anthropic', 'ollama'

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_HOST=http://localhost:11434
```

### Programmatic Configuration
```python
agent = Agent(
    name="Katrina",
    llm_provider="ollama",
    llm_config={
        # OpenAI settings
        'openai_api_key': 'sk-...',
        'openai_model': 'gpt-3.5-turbo',
        'openai_config': {
            'temperature': 0.7,
            'max_tokens': 500
        },
        
        # Anthropic settings
        'anthropic_api_key': 'sk-ant-...',
        'anthropic_model': 'claude-3-sonnet-20240229',
        'anthropic_config': {
            'temperature': 0.7,
            'max_tokens': 500
        },
        
        # Ollama settings
        'ollama_model': 'llama2',
        'ollama_host': 'http://localhost:11434',
        'ollama_config': {
            'temperature': 0.7,
            'num_predict': 500
        }
    }
)
```

## Architecture

### LLM Provider Hierarchy
```
BaseLLMProvider (Abstract)
├── OpenAIProvider
├── AnthropicProvider
└── OllamaProvider
```

### Integration Points
```
Agent
├── ReasoningEngine (uses LLM for thinking/reflection)
│   └── LLMManager (selects and manages providers)
│       ├── OpenAIProvider
│       ├── AnthropicProvider
│       └── OllamaProvider
├── SkillManager (unchanged)
└── MemoryManager (unchanged)
```

### How LLM Enhances the Agent

1. **Chain-of-Thought Reasoning**: LLM generates detailed reasoning about observations and context
2. **Reflection**: LLM provides thoughtful analysis of action results
3. **Planning**: LLM can help create more sophisticated plans
4. **Fallback**: If LLM unavailable, agent uses basic rule-based reasoning

## Best Practices

### 1. Start with Ollama
- Free and private
- No API keys needed
- Good performance for most tasks
- Easy to set up

### 2. Use .env for API Keys
```bash
# Never commit API keys to git
# Use .env file (already in .gitignore)
echo "OPENAI_API_KEY=sk-..." >> .env
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### 3. Handle Failures Gracefully
```python
agent = Agent(
    name="Katrina",
    llm_provider="ollama"  # Will fallback to basic mode if Ollama unavailable
)

# Agent still works even if LLM fails
response = agent.process("calculate 5 + 3")
```

### 4. Choose the Right Model

**For Fast, Simple Tasks:**
- Ollama: `llama2`, `mistral`
- OpenAI: `gpt-3.5-turbo`
- Anthropic: `claude-3-haiku`

**For Complex Reasoning:**
- Ollama: `llama2:70b`, `mixtral`
- OpenAI: `gpt-4`, `gpt-4-turbo`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`

**For Code-Related Tasks:**
- Ollama: `codellama`
- OpenAI: `gpt-4`
- Anthropic: `claude-3-opus`

## Troubleshooting

### Ollama Issues

**Problem**: "Ollama provider not available"
```bash
# Solution 1: Check if Ollama is running
curl http://localhost:11434/api/tags

# Solution 2: Start Ollama
ollama serve

# Solution 3: Pull the model
ollama pull llama2
```

**Problem**: "Connection refused"
```bash
# Check if Ollama is running on correct port
ps aux | grep ollama

# Restart Ollama
killall ollama
ollama serve
```

### OpenAI Issues

**Problem**: "OpenAI provider not available"
```bash
# Solution 1: Install package
pip install openai

# Solution 2: Check API key
echo $OPENAI_API_KEY

# Solution 3: Set API key
export OPENAI_API_KEY="sk-..."
```

**Problem**: "Rate limit exceeded"
```python
# Use basic mode temporarily
agent.llm_manager.switch_provider('none')
```

### Anthropic Issues

**Problem**: "Anthropic provider not available"
```bash
# Solution 1: Install package
pip install anthropic

# Solution 2: Check API key
echo $ANTHROPIC_API_KEY

# Solution 3: Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Performance Considerations

### Latency
- **Basic mode**: ~10ms (no LLM)
- **Ollama**: ~500ms-2s (depends on model and hardware)
- **OpenAI**: ~500ms-2s (depends on network and load)
- **Anthropic**: ~500ms-2s (depends on network and load)

### Cost
- **Basic mode**: Free
- **Ollama**: Free (uses local resources)
- **OpenAI**: $0.0005-$0.03 per 1K tokens (depends on model)
- **Anthropic**: $0.003-$0.075 per 1K tokens (depends on model)

### Privacy
- **Basic mode**: Completely private
- **Ollama**: Completely private (local processing)
- **OpenAI**: Data sent to OpenAI servers
- **Anthropic**: Data sent to Anthropic servers

## FAQ

**Q: Do I need an LLM to use the agent?**
A: No! The agent works perfectly without any LLM in basic mode.

**Q: Which provider should I use?**
A: Start with Ollama (free, local, private). Use cloud providers only if you need their specific capabilities.

**Q: Can I use multiple providers?**
A: Yes! You can switch between providers at runtime using `agent.llm_manager.switch_provider()`.

**Q: What if my API key runs out?**
A: The agent will automatically fall back to basic mode and continue working.

**Q: Is my data private with Ollama?**
A: Yes! Ollama runs completely locally. Nothing is sent to external servers.

**Q: Can I use custom Ollama models?**
A: Yes! Any model available in Ollama can be used. Run `ollama list` to see installed models.

**Q: How do I know which provider is being used?**
A: Check `agent.llm_manager.get_current_provider_name()` or look at the initialization output.

## Examples

Run the complete example:
```bash
python examples/llm_integration_example.py
```

This demonstrates all three providers and various usage patterns.
