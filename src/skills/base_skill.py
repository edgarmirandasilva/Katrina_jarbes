"""
Base Skill Interface
All skills must inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Skill(ABC):
    """Base class for all agent skills/plugins"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = ""
        self.parameters = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with given parameters
        
        Returns:
            Dict with 'success' (bool) and 'result' (any) keys
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Return the skill schema for tool calling
        
        Returns:
            Dict with function name, description, and parameters
        """
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Validate if required parameters are provided"""
        required = self.parameters.get('required', [])
        return all(param in kwargs for param in required)
