"""
Example: Custom Skill Creation
Demonstrates how to create and register a custom skill
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agent import Agent
from src.skills import Skill
from typing import Dict, Any


class WeatherSkill(Skill):
    """Example custom skill for weather information"""
    
    def __init__(self):
        super().__init__()
        self.description = "Get weather information (simulated)"
        self.parameters = {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'Location to get weather for'
                }
            },
            'required': ['location']
        }
    
    def execute(self, location: str, **kwargs) -> Dict[str, Any]:
        """Execute weather lookup (simulated)"""
        # In a real implementation, this would call a weather API
        weather_data = {
            'london': '☁️ Cloudy, 15°C',
            'paris': '☀️ Sunny, 22°C',
            'tokyo': '🌧️ Rainy, 18°C',
            'new york': '⛅ Partly Cloudy, 20°C'
        }
        
        location_lower = location.lower()
        weather = weather_data.get(location_lower, '❓ Weather data not available')
        
        return {
            'success': True,
            'location': location,
            'weather': weather
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the skill schema"""
        return {
            'name': 'weather',
            'description': self.description,
            'parameters': self.parameters
        }


def main():
    """Demonstrate custom skill creation"""
    
    print("="*60)
    print("🔧 Custom Skill Example")
    print("="*60)
    
    # Initialize agent
    agent = Agent(name="Katrina", memory_dir="./memory_store")
    
    # Create and register custom skill
    weather_skill = WeatherSkill()
    agent.skill_manager.register_skill(weather_skill)
    
    print("\n✅ Custom weather skill registered!")
    print(f"Available skills: {agent.skill_manager.list_skills()}")
    
    # Test the custom skill
    print("\n🌤️ Testing weather skill:")
    result = agent.skill_manager.execute_skill('weather', location='London')
    print(f"Result: {result}")
    
    # Note: To use the skill through natural language, 
    # you would need to extend the NLP processor with weather patterns
    print("\n💡 To use this skill through natural language, extend the NLP processor")
    print("   with patterns like: r'weather\\s+in\\s+(.+)'")


if __name__ == "__main__":
    main()
