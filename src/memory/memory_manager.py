"""
Memory Manager - Coordinates short-term and long-term memory
"""

from typing import List, Dict, Any
from .short_term_memory import ShortTermMemory
from .long_term_memory import LongTermMemory


class MemoryManager:
    """Coordinates between short-term and long-term memory"""
    
    def __init__(self, storage_dir: str = "./memory_store", max_short_term: int = 50):
        self.short_term = ShortTermMemory(max_messages=max_short_term)
        self.long_term = LongTermMemory(storage_dir=storage_dir)
    
    def add_interaction(self, user_input: str, agent_response: str, metadata: Dict[str, Any] = None):
        """Add an interaction to both short and long-term memory"""
        # Add to short-term memory
        self.short_term.add_message('user', user_input, metadata)
        self.short_term.add_message('assistant', agent_response, metadata)
        
        # Store important interactions in long-term memory
        interaction_text = f"User: {user_input}\nAssistant: {agent_response}"
        self.long_term.store(interaction_text, metadata)
    
    def get_conversation_context(self, last_n: int = 10) -> str:
        """Get recent conversation context"""
        return self.short_term.get_context_window()
    
    def search_long_term_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search through long-term memory"""
        return self.long_term.search(query, max_results)
    
    def store_knowledge(self, content: str, metadata: Dict[str, Any] = None):
        """Store knowledge in long-term memory"""
        return self.long_term.store(content, metadata)
    
    def get_recent_memories(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get recent long-term memories"""
        return self.long_term.get_recent(n)
    
    def clear_short_term(self):
        """Clear short-term memory"""
        self.short_term.clear()
    
    def summary(self) -> str:
        """Get summary of memory state"""
        return f"{self.short_term.summary()}\n{self.long_term.summary()}"
