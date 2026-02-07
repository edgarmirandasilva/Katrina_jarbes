"""
Natural Language Processor - Parses and understands natural language commands
"""

import re
from typing import Dict, Any, List


class NaturalLanguageProcessor:
    """Processes natural language to extract intent and entities"""
    
    def __init__(self):
        # Define intent patterns
        self.intent_patterns = {
            'calculate': [
                r'calculate\s+(.+)',
                r'what\s+is\s+(.+)',
                r'compute\s+(.+)',
                r'solve\s+(.+)',
                r'\d+\s*[\+\-\*\/]\s*\d+'
            ],
            'file_read': [
                r'read\s+(?:file\s+)?(.+)',
                r'show\s+(?:me\s+)?(?:file\s+)?(.+)',
                r'open\s+(?:file\s+)?(.+)',
                r'display\s+(?:file\s+)?(.+)'
            ],
            'file_write': [
                r'write\s+(.+)\s+to\s+(?:file\s+)?(.+)',
                r'save\s+(.+)\s+to\s+(?:file\s+)?(.+)',
                r'create\s+(?:file\s+)?(.+)\s+with\s+(.+)'
            ],
            'file_list': [
                r'list\s+files',
                r'show\s+files',
                r'what\s+files',
                r'files\s+in\s+workspace'
            ],
            'search': [
                r'search\s+(?:for\s+)?(.+)',
                r'find\s+(.+)',
                r'look\s+for\s+(.+)',
                r'remember\s+(.+)'
            ],
            'help': [
                r'help',
                r'what\s+can\s+you\s+do',
                r'capabilities',
                r'commands'
            ]
        }
    
    def parse(self, user_input: str) -> Dict[str, Any]:
        """
        Parse natural language input to extract intent and parameters
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Dict with 'intent', 'entities', and 'confidence'
        """
        user_input_lower = user_input.lower().strip()
        
        # Try to match intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    entities = self._extract_entities(intent, match, user_input)
                    return {
                        'intent': intent,
                        'entities': entities,
                        'confidence': 0.9,
                        'original_input': user_input
                    }
        
        # No clear intent found
        return {
            'intent': 'unknown',
            'entities': {},
            'confidence': 0.3,
            'original_input': user_input
        }
    
    def _extract_entities(self, intent: str, match: re.Match, original_input: str) -> Dict[str, Any]:
        """Extract entities based on intent and regex match"""
        entities = {}
        
        if intent == 'calculate':
            if match.groups():
                entities['expression'] = match.group(1).strip()
            else:
                # Extract the mathematical expression
                entities['expression'] = match.group(0).strip()
        
        elif intent == 'file_read':
            if match.groups():
                entities['filename'] = match.group(1).strip()
        
        elif intent == 'file_write':
            if len(match.groups()) >= 2:
                entities['content'] = match.group(1).strip()
                entities['filename'] = match.group(2).strip()
        
        elif intent == 'search':
            if match.groups():
                entities['query'] = match.group(1).strip()
        
        return entities
    
    def intent_to_tool(self, intent: str) -> str:
        """Map intent to tool name"""
        intent_tool_map = {
            'calculate': 'calculator',
            'file_read': 'file_operations',
            'file_write': 'file_operations',
            'file_list': 'file_operations',
            'search': 'knowledge_search',
            'help': None
        }
        return intent_tool_map.get(intent)
    
    def get_tool_parameters(self, parse_result: Dict[str, Any]) -> Dict[str, Any]:
        """Convert parsed result to tool parameters"""
        intent = parse_result['intent']
        entities = parse_result['entities']
        
        if intent == 'calculate':
            return {'expression': entities.get('expression', '')}
        
        elif intent == 'file_read':
            return {
                'operation': 'read',
                'filename': entities.get('filename', '')
            }
        
        elif intent == 'file_write':
            return {
                'operation': 'write',
                'filename': entities.get('filename', ''),
                'content': entities.get('content', '')
            }
        
        elif intent == 'file_list':
            return {'operation': 'list'}
        
        elif intent == 'search':
            return {
                'query': entities.get('query', ''),
                'max_results': 5
            }
        
        return {}
