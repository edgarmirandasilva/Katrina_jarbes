"""
Short-term Memory - Manages conversation history and context
"""

from typing import List, Dict, Any
from collections import deque


class ShortTermMemory:
    """Manages recent conversation history and context"""
    
    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.messages: deque = deque(maxlen=max_messages)
        self.context: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a message to short-term memory"""
        message = {
            'role': role,
            'content': content,
            'metadata': metadata or {}
        }
        self.messages.append(message)
    
    def get_messages(self, last_n: int = None) -> List[Dict[str, Any]]:
        """Get recent messages"""
        if last_n:
            return list(self.messages)[-last_n:]
        return list(self.messages)
    
    def get_context_window(self) -> str:
        """Get formatted context window for the agent"""
        context_str = "Recent conversation:\n"
        for msg in self.messages:
            role = msg['role'].capitalize()
            content = msg['content']
            context_str += f"{role}: {content}\n"
        return context_str
    
    def clear(self):
        """Clear short-term memory"""
        self.messages.clear()
        self.context.clear()
    
    def set_context(self, key: str, value: Any):
        """Set a context variable"""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context variable"""
        return self.context.get(key, default)
    
    def summary(self) -> str:
        """Get a summary of short-term memory"""
        return f"Short-term memory: {len(self.messages)} messages, {len(self.context)} context variables"
