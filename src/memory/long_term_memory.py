"""
Long-term Memory - Manages persistent memory with embeddings
"""

import os
import json
import pickle
from typing import List, Dict, Any
from datetime import datetime


class LongTermMemory:
    """Manages persistent memory storage with simple text-based search"""
    
    def __init__(self, storage_dir: str = "./memory_store"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        self.memories_file = os.path.join(storage_dir, "memories.json")
        self.memories: List[Dict[str, Any]] = []
        self._load_memories()
    
    def _load_memories(self):
        """Load memories from disk"""
        if os.path.exists(self.memories_file):
            try:
                with open(self.memories_file, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
                print(f"Loaded {len(self.memories)} memories from disk")
            except Exception as e:
                print(f"Error loading memories: {e}")
                self.memories = []
    
    def _save_memories(self):
        """Save memories to disk"""
        try:
            with open(self.memories_file, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memories: {e}")
    
    def store(self, content: str, metadata: Dict[str, Any] = None):
        """Store a new memory"""
        memory = {
            'id': len(self.memories),
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        self.memories.append(memory)
        self._save_memories()
        return memory['id']
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Simple text-based search through memories
        Returns most relevant memories based on keyword matching
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score each memory based on keyword matches
        scored_memories = []
        for memory in self.memories:
            content_lower = memory['content'].lower()
            content_words = set(content_lower.split())
            
            # Calculate relevance score
            common_words = query_words.intersection(content_words)
            score = len(common_words)
            
            # Bonus for exact phrase match
            if query_lower in content_lower:
                score += 10
            
            if score > 0:
                scored_memories.append((score, memory))
        
        # Sort by score and return top results
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        results = [mem for score, mem in scored_memories[:max_results]]
        
        # Update access count
        for result in results:
            result['access_count'] += 1
        
        self._save_memories()
        return results
    
    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get most recent memories"""
        return self.memories[-n:] if self.memories else []
    
    def clear(self):
        """Clear all memories"""
        self.memories = []
        self._save_memories()
    
    def summary(self) -> str:
        """Get a summary of long-term memory"""
        return f"Long-term memory: {len(self.memories)} memories stored"
