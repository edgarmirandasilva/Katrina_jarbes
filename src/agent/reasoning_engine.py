"""
Reasoning Engine - Implements Chain-of-Thought and Reflection
"""

from typing import List, Dict, Any
import json


class ReasoningEngine:
    """Implements chain-of-thought reasoning and reflection"""
    
    def __init__(self):
        self.thought_chain: List[str] = []
        self.reflections: List[str] = []
    
    def think(self, observation: str, context: str = "") -> str:
        """
        Generate chain-of-thought reasoning
        
        Args:
            observation: Current observation or input
            context: Additional context
            
        Returns:
            Reasoning thought
        """
        thought = f"Observation: {observation}\n"
        
        if context:
            thought += f"Context: {context}\n"
        
        # Analyze what we know
        thought += "Analysis: "
        
        self.thought_chain.append(thought)
        return thought
    
    def reflect(self, action_result: Dict[str, Any]) -> str:
        """
        Reflect on the result of an action
        
        Args:
            action_result: Result from executing an action
            
        Returns:
            Reflection on the result
        """
        success = action_result.get('success', False)
        
        if success:
            reflection = f"Action succeeded. Result: {action_result.get('result', 'N/A')}"
        else:
            error = action_result.get('error', 'Unknown error')
            reflection = f"Action failed. Error: {error}. Need to try a different approach."
        
        self.reflections.append(reflection)
        return reflection
    
    def plan(self, goal: str, available_tools: List[str]) -> List[Dict[str, str]]:
        """
        Create a plan to achieve a goal
        
        Args:
            goal: The goal to achieve
            available_tools: List of available tool names
            
        Returns:
            List of planned steps
        """
        # Simple planning - break down goal into steps
        plan = [
            {
                'step': 1,
                'description': 'Analyze the goal and understand requirements',
                'status': 'pending'
            },
            {
                'step': 2,
                'description': 'Select appropriate tool for the task',
                'status': 'pending'
            },
            {
                'step': 3,
                'description': 'Execute the tool with proper parameters',
                'status': 'pending'
            },
            {
                'step': 4,
                'description': 'Verify the result and reflect on outcome',
                'status': 'pending'
            }
        ]
        
        return plan
    
    def should_continue(self, iteration: int, max_iterations: int, goal_achieved: bool) -> bool:
        """
        Decide if agent should continue iterating
        
        Args:
            iteration: Current iteration number
            max_iterations: Maximum allowed iterations
            goal_achieved: Whether the goal has been achieved
            
        Returns:
            True if should continue, False otherwise
        """
        if goal_achieved:
            return False
        
        if iteration >= max_iterations:
            return False
        
        return True
    
    def get_thought_chain(self) -> List[str]:
        """Get the complete thought chain"""
        return self.thought_chain
    
    def get_reflections(self) -> List[str]:
        """Get all reflections"""
        return self.reflections
    
    def clear(self):
        """Clear reasoning history"""
        self.thought_chain.clear()
        self.reflections.clear()
