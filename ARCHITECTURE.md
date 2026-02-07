# Architecture Documentation

## System Overview

The Katrina Agent is a modular Python-based AI agent system that implements modern agent techniques including tool calling, chain-of-thought reasoning, reflection, planning, and action loops.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                           │
│                   (Natural Language)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   NLP PROCESSOR                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Parse natural language                            │   │
│  │  • Extract intent (calculate, file_ops, search, etc)│   │
│  │  • Extract entities (parameters)                     │   │
│  │  • Map intent to tools                               │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT CORE                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ACTION LOOP                             │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ 1. THINK (Chain-of-Thought)                    │  │   │
│  │  │    - Analyze situation                         │  │   │
│  │  │    - Consider context                          │  │   │
│  │  │    - Plan approach                             │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ 2. ACT (Tool Calling)                          │  │   │
│  │  │    - Select appropriate skill                  │  │   │
│  │  │    - Prepare parameters                        │  │   │
│  │  │    - Execute skill                             │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ 3. REFLECT                                     │  │   │
│  │  │    - Analyze result                            │  │   │
│  │  │    - Check if goal achieved                    │  │   │
│  │  │    - Decide next action                        │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  │                                                    │   │
│  │  └─────► Loop until goal achieved or max iterations │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  SKILL MANAGER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Dynamic skill loading                             │   │
│  │  • Skill registration                                │   │
│  │  • Tool calling execution                            │   │
│  │  • Schema management                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────┬─────────────────┬──────────────────┬──────────────────┘
     │                 │                  │
     ▼                 ▼                  ▼
┌──────────┐    ┌──────────┐      ┌──────────────┐
│Calculator│    │   File   │      │  Knowledge   │
│  Skill   │    │Operations│      │    Search    │
└──────────┘    └──────────┘      └──────────────┘
     │                 │                  │
     └─────────────────┴──────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  MEMORY MANAGER                             │
│  ┌──────────────────────┐    ┌────────────────────────┐     │
│  │  SHORT-TERM MEMORY   │    │  LONG-TERM MEMORY      │     │
│  │  • Recent messages   │    │  • Persistent storage  │     │
│  │  • Context variables │    │  • JSON file-based     │     │
│  │  • In-memory queue   │    │  • Searchable          │     │
│  │  • Max 50 messages   │    │  • Access tracking     │     │
│  └──────────────────────┘    └────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESPONSE                                 │
│                (Natural Language)                           │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Input Processing Flow

```
User Input
    │
    ├─► NLP Processor
    │       │
    │       ├─► Intent Recognition
    │       ├─► Entity Extraction
    │       └─► Tool Mapping
    │
    └─► Short-term Memory (store user message)
```

### 2. Action Loop Flow

```
Parse Result
    │
    ├─► Reasoning Engine
    │       │
    │       ├─► Chain-of-Thought
    │       │       └─► Generate reasoning trace
    │       │
    │       ├─► Planning
    │       │       └─► Create action plan
    │       │
    │       └─► Should Continue?
    │               ├─► Yes: Next iteration
    │               └─► No: Exit loop
    │
    ├─► Skill Manager
    │       │
    │       └─► Execute Tool
    │               └─► Return result
    │
    └─► Reflection
            │
            ├─► Success? → Format response
            └─► Failure? → Try alternative or report error
```

### 3. Memory Storage Flow

```
Interaction Complete
    │
    ├─► Short-term Memory
    │       └─► Add message to queue
    │
    └─► Long-term Memory
            └─► Store interaction with metadata
```

## Module Breakdown

### src/agent/

#### agent_core.py
- **Class:** `Agent`
- **Purpose:** Main orchestrator
- **Key Methods:**
  - `process()`: Main entry point
  - `_action_loop()`: Iterative execution
  - `_format_success_response()`: Response formatting
  - `get_status()`: Status reporting

#### reasoning_engine.py
- **Class:** `ReasoningEngine`
- **Purpose:** Implements CoT, reflection, planning
- **Key Methods:**
  - `think()`: Chain-of-thought generation
  - `reflect()`: Action result reflection
  - `plan()`: Goal planning
  - `should_continue()`: Loop control

#### nlp_processor.py
- **Class:** `NaturalLanguageProcessor`
- **Purpose:** Natural language understanding
- **Key Methods:**
  - `parse()`: Intent and entity extraction
  - `intent_to_tool()`: Intent-to-tool mapping
  - `get_tool_parameters()`: Parameter extraction

### src/memory/

#### short_term_memory.py
- **Class:** `ShortTermMemory`
- **Purpose:** Recent conversation history
- **Storage:** In-memory deque
- **Capacity:** Configurable (default 50 messages)

#### long_term_memory.py
- **Class:** `LongTermMemory`
- **Purpose:** Persistent knowledge storage
- **Storage:** JSON file
- **Features:** Text search, access tracking

#### memory_manager.py
- **Class:** `MemoryManager`
- **Purpose:** Coordinate memory systems
- **Features:** Dual memory management, search

### src/skills/

#### base_skill.py
- **Class:** `Skill` (ABC)
- **Purpose:** Base interface for all skills
- **Required Methods:**
  - `execute()`: Execute skill logic
  - `get_schema()`: Return tool schema

#### calculator_skill.py
- **Class:** `CalculatorSkill`
- **Purpose:** Safe mathematical calculations
- **Features:** AST-based safe evaluation

#### file_operations_skill.py
- **Class:** `FileOperationsSkill`
- **Purpose:** File system operations
- **Operations:** read, write, list
- **Security:** Sandboxed to workspace directory

#### knowledge_search_skill.py
- **Class:** `KnowledgeSearchSkill`
- **Purpose:** Search long-term memory
- **Features:** Keyword-based search

#### skill_manager.py
- **Class:** `SkillManager`
- **Purpose:** Skill orchestration
- **Features:** Dynamic loading, registration, execution

## Design Patterns

### 1. Strategy Pattern
Skills implement a common interface, allowing dynamic selection and execution.

### 2. Observer Pattern
Memory manager observes interactions and stores them.

### 3. Chain of Responsibility
NLP → Reasoning → Action → Reflection forms a processing chain.

### 4. Plugin Architecture
Skills are plugins that can be dynamically loaded and registered.

## Key Features Implementation

### Tool Calling
- Skills expose schemas compatible with function calling
- Agent dynamically selects and calls appropriate tools
- Parameters extracted from natural language

### Chain-of-Thought
- Explicit reasoning trace before action
- Context-aware thinking
- Transparent decision making

### Reflection
- Post-action analysis
- Success/failure evaluation
- Alternative strategy consideration

### Planning
- Goal decomposition
- Step-by-step planning
- Resource consideration

### Action Loops
- Iterative goal pursuit
- Max iteration limit
- Early termination on success

## Extension Points

### Adding New Skills
1. Inherit from `Skill` base class
2. Implement `execute()` and `get_schema()`
3. Register with `SkillManager`

### Adding New Intents
1. Add patterns to `NaturalLanguageProcessor.intent_patterns`
2. Add mapping in `intent_to_tool()`
3. Add parameter extraction in `get_tool_parameters()`

### Custom Memory Backends
1. Inherit from `LongTermMemory`
2. Override `store()` and `search()` methods
3. Replace in `MemoryManager`

### Alternative Reasoning Strategies
1. Inherit from `ReasoningEngine`
2. Override `think()`, `reflect()`, `plan()` methods
3. Replace in `Agent`

## Performance Considerations

### Memory
- Short-term: O(1) append, O(n) retrieval
- Long-term: O(n) search (can be optimized with embeddings)

### Computation
- Action loop: O(m * n) where m = iterations, n = tool complexity
- NLP parsing: O(p) where p = number of patterns

### Storage
- Short-term: In-memory only
- Long-term: JSON file (can grow large)

## Security Considerations

### File Operations
- Sandboxed to workspace directory
- Path traversal prevention
- No system file access

### Calculator
- AST-based evaluation (no eval/exec)
- Limited to mathematical operations
- No arbitrary code execution

### Memory
- Local storage only
- No external data transmission
- User data stays on device

## Future Enhancements

1. **Vector Embeddings**: Replace text search with semantic search
2. **LLM Integration**: Add OpenAI/Anthropic for better reasoning
3. **Async Execution**: Parallel skill execution
4. **Web Interface**: Streamlit/Gradio UI
5. **Advanced Planning**: PDDL-based planning
6. **Multi-agent**: Agent collaboration
7. **Learning**: Improve from past interactions
