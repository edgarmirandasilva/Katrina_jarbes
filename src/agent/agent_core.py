"""
Agent Core - Main agent orchestrator implementing the action loop
Enhanced with optional LLM integration for improved reasoning
"""

from typing import Dict, Any, List, Optional
from .reasoning_engine import ReasoningEngine
from .nlp_processor import NaturalLanguageProcessor
from ..memory.memory_manager import MemoryManager
from ..skills.skill_manager import SkillManager


class Agent:
    """
    Main agent class implementing modern agent techniques:
    - Tool calling
    - Chain-of-thought reasoning
    - Reflection
    - Planning
    - Action loops
    - Optional LLM integration (OpenAI, Anthropic, Ollama)
    """
    
    def __init__(self, 
                 name: str = "Katrina", 
                 memory_dir: str = "./memory_store", 
                 max_iterations: int = 10,
                 llm_provider: str = "none",
                 llm_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent
        
        Args:
            name: Agent name
            memory_dir: Directory for persistent memory
            max_iterations: Maximum action loop iterations
            llm_provider: LLM provider to use ('openai', 'anthropic', 'ollama', or 'none')
                        Default: 'none' (agent works without LLM)
            llm_config: Optional LLM configuration dict with keys:
                       - openai_api_key: OpenAI API key
                       - anthropic_api_key: Anthropic API key
                       - openai_model: OpenAI model name
                       - anthropic_model: Anthropic model name
                       - ollama_model: Ollama model name
                       - ollama_host: Ollama server URL
        """
        self.name = name
        self.max_iterations = max_iterations
        
        # Initialize LLM if requested
        self.llm_manager = None
        if llm_provider.lower() != "none":
            try:
                from ..llm import LLMManager
                llm_config = llm_config or {}
                self.llm_manager = LLMManager(
                    preferred_provider=llm_provider,
                    **llm_config
                )
            except Exception as e:
                print(f"Warning: Failed to initialize LLM: {e}")
                print("Agent will work in basic mode without LLM")
        
        # Initialize components
        self.memory = MemoryManager(storage_dir=memory_dir)
        self.skill_manager = SkillManager(memory_manager=self.memory)
        self.reasoning = ReasoningEngine(llm_manager=self.llm_manager)
        self.nlp = NaturalLanguageProcessor()
        
        print(f"Agent '{self.name}' initialized")
        if self.llm_manager and self.llm_manager.is_enabled():
            provider = self.llm_manager.get_current_provider_name()
            print(f"LLM enabled: {provider}")
        else:
            print("LLM disabled: agent will work in basic mode")
        print(f"Available skills: {self.skill_manager.list_skills()}")
    
    def process(self, user_input: str, verbose: bool = True) -> str:
        """
        Process user input through the agent pipeline
        
        Args:
            user_input: Natural language input from user
            verbose: Whether to print detailed reasoning
            
        Returns:
            Agent's response
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"User: {user_input}")
            print(f"{'='*60}")
        
        # Parse natural language
        parse_result = self.nlp.parse(user_input)
        intent = parse_result['intent']
        
        if verbose:
            print(f"\n[NLP] Intent: {intent}")
            print(f"[NLP] Entities: {parse_result['entities']}")
        
        # Special handling for help
        if intent == 'help':
            return self._handle_help()
        
        # Special handling for unknown intent
        if intent == 'unknown':
            return self._handle_unknown(user_input)
        
        # Execute action loop
        response = self._action_loop(parse_result, verbose)
        
        # Store interaction in memory
        self.memory.add_interaction(user_input, response)
        
        return response
    
    def _action_loop(self, parse_result: Dict[str, Any], verbose: bool) -> str:
        """
        Execute the agent's action loop with planning and reflection
        """
        iteration = 0
        goal_achieved = False
        result = None
        
        # Get tool and parameters
        tool_name = self.nlp.intent_to_tool(parse_result['intent'])
        tool_params = self.nlp.get_tool_parameters(parse_result)
        
        if not tool_name:
            return "I'm not sure how to handle that request."
        
        while iteration < self.max_iterations and not goal_achieved:
            iteration += 1
            
            if verbose:
                print(f"\n[Action Loop] Iteration {iteration}")
            
            # Chain-of-thought reasoning
            thought = self.reasoning.think(
                f"Need to use {tool_name} with parameters {tool_params}",
                context=self.memory.get_conversation_context(last_n=5)
            )
            
            if verbose:
                print(f"[Reasoning] {thought}")
            
            # Execute tool
            if verbose:
                print(f"[Tool Call] Executing {tool_name}...")
            
            result = self.skill_manager.execute_skill(tool_name, **tool_params)
            
            # Reflect on result
            reflection = self.reasoning.reflect(result)
            
            if verbose:
                print(f"[Reflection] {reflection}")
            
            # Check if goal achieved
            if result.get('success'):
                goal_achieved = True
            else:
                # Could try alternative approaches here
                break
        
        # Format response
        if result and result.get('success'):
            return self._format_success_response(parse_result['intent'], result)
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Failed to execute'
            return f"I encountered an error: {error_msg}"
    
    def _format_success_response(self, intent: str, result: Dict[str, Any]) -> str:
        """Format successful result into natural language response"""
        if intent == 'calculate':
            expr = result.get('expression', '')
            res = result.get('result', '')
            return f"The result of {expr} is {res}"
        
        elif intent == 'file_read':
            filename = result.get('filename', '')
            content = result.get('content', '')
            return f"Content of {filename}:\n{content}"
        
        elif intent == 'file_write':
            filename = result.get('filename', '')
            return f"Successfully wrote to {filename}"
        
        elif intent == 'file_list':
            files = result.get('files', [])
            if files:
                return f"Files in workspace: {', '.join(files)}"
            else:
                return "No files in workspace"
        
        elif intent == 'search':
            results = result.get('results', [])
            count = result.get('count', 0)
            if count > 0:
                response = f"Found {count} relevant memories:\n"
                for i, mem in enumerate(results[:3], 1):
                    content = mem.get('content', '')[:100]
                    response += f"{i}. {content}...\n"
                return response
            else:
                return "No relevant memories found"
        
        return f"Task completed successfully: {result}"
    
    def _handle_help(self) -> str:
        """Handle help request"""
        skills = self.skill_manager.list_skills()
        help_text = f"I'm {self.name}, your AI agent. I can help you with:\n\n"
        help_text += "📊 Calculations: 'calculate 5 + 3', 'what is 10 * 20'\n"
        help_text += "📁 File operations: 'list files', 'read file notes.txt', 'write hello to file.txt'\n"
        help_text += "🔍 Search memories: 'search for Python', 'find information about AI'\n"
        help_text += f"\nAvailable skills: {', '.join(skills)}"
        return help_text
    
    def _handle_unknown(self, user_input: str) -> str:
        """Handle unknown intent"""
        # Try to search memory for relevant information
        memories = self.memory.search_long_term_memory(user_input, max_results=3)
        
        if memories:
            response = "I'm not sure exactly what you mean, but here's what I found in my memory:\n"
            for mem in memories:
                content = mem.get('content', '')[:100]
                response += f"- {content}...\n"
            return response
        else:
            return "I'm not sure how to help with that. Try 'help' to see what I can do."
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            'name': self.name,
            'skills': self.skill_manager.list_skills(),
            'memory_summary': self.memory.summary(),
            'thought_chain_length': len(self.reasoning.get_thought_chain()),
            'reflections_count': len(self.reasoning.get_reflections())
        }
    
    def reset(self):
        """Reset agent state"""
        self.memory.clear_short_term()
        self.reasoning.clear()
        print(f"Agent '{self.name}' reset")
