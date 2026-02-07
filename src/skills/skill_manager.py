"""
Skill Manager - Loads and manages all available skills
"""

from typing import Dict, List, Any
from .base_skill import Skill
from .calculator_skill import CalculatorSkill
from .file_operations_skill import FileOperationsSkill
from .knowledge_search_skill import KnowledgeSearchSkill


class SkillManager:
    """Manages all available skills/plugins"""
    
    def __init__(self, memory_manager=None):
        self.skills: Dict[str, Skill] = {}
        self.memory_manager = memory_manager
        self._load_default_skills()
    
    def _load_default_skills(self):
        """Load default skills"""
        self.register_skill(CalculatorSkill())
        self.register_skill(FileOperationsSkill())
        if self.memory_manager:
            self.register_skill(KnowledgeSearchSkill(self.memory_manager))
    
    def register_skill(self, skill: Skill):
        """Register a new skill"""
        schema = skill.get_schema()
        skill_name = schema['name']
        self.skills[skill_name] = skill
        print(f"Registered skill: {skill_name}")
    
    def get_skill(self, name: str) -> Skill:
        """Get a skill by name"""
        return self.skills.get(name)
    
    def list_skills(self) -> List[str]:
        """List all available skills"""
        return list(self.skills.keys())
    
    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all skills (for tool calling)"""
        return [skill.get_schema() for skill in self.skills.values()]
    
    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a skill by name"""
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                'success': False,
                'error': f'Skill not found: {skill_name}'
            }
        
        return skill.execute(**kwargs)
