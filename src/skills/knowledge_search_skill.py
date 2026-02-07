"""
Knowledge Search Skill - Search in knowledge base
"""

from typing import Dict, Any, List
from .base_skill import Skill


class KnowledgeSearchSkill(Skill):
    """Search through stored knowledge and memories"""
    
    def __init__(self, memory_manager=None):
        super().__init__()
        self.description = "Search through stored knowledge and previous conversations"
        self.memory_manager = memory_manager
        
        self.parameters = {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'Search query to find relevant information'
                },
                'max_results': {
                    'type': 'integer',
                    'description': 'Maximum number of results to return (default: 5)'
                }
            },
            'required': ['query']
        }
    
    def execute(self, query: str, max_results: int = 5, **kwargs) -> Dict[str, Any]:
        """Search through knowledge base"""
        try:
            if not self.memory_manager:
                return {
                    'success': False,
                    'error': 'Memory manager not initialized'
                }
            
            results = self.memory_manager.search_long_term_memory(query, max_results)
            
            return {
                'success': True,
                'query': query,
                'results': results,
                'count': len(results)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the skill schema"""
        return {
            'name': 'knowledge_search',
            'description': self.description,
            'parameters': self.parameters
        }
