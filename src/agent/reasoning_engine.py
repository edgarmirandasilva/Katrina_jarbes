"""
Reasoning Engine - Implements Chain-of-Thought and Reflection
Enhanced with optional LLM integration for improved reasoning
"""

from typing import List, Dict, Any, Optional
import json


class ReasoningEngine:
    """Implements chain-of-thought reasoning and reflection with optional LLM support"""
    
    def __init__(self, llm_manager=None):
        """
        Initialize reasoning engine
        
        Args:
            llm_manager: Optional LLMManager instance for enhanced reasoning
        """
        self.thought_chain: List[str] = []
        self.reflections: List[str] = []
        self.llm_manager = llm_manager
    
    def think(self, observation: str, context: str = "") -> str:
        """
        Generate chain-of-thought reasoning
        
        Args:
            observation: Current observation or input
            context: Additional context
            
        Returns:
            Reasoning thought
        """
        # If LLM is available, use it for enhanced reasoning
        if self.llm_manager and self.llm_manager.is_enabled():
            thought = self._llm_think(observation, context)
        else:
            # Fallback to basic reasoning
            thought = f"Observation: {observation}\n"
            
            if context:
                thought += f"Context: {context}\n"
            
            # Analyze what we know
            thought += "Analysis: Will proceed with the task based on available information."
        
        self.thought_chain.append(thought)
        return thought
    
    def _llm_think(self, observation: str, context: str) -> str:
        """
        Use LLM for chain-of-thought reasoning
        
        Args:
            observation: Current observation
            context: Additional context
            
        Returns:
            LLM-generated reasoning
        """
        prompt = f"""You are an AI agent's reasoning module. Analyze the situation and provide clear reasoning.

Observation: {observation}

Context: {context if context else 'No additional context'}

Provide a concise analysis (2-3 sentences) of what you observe and how to approach this task."""

        try:
            response = self.llm_manager.generate(prompt, temperature=0.7, max_tokens=150)
            if response:
                return f"Observation: {observation}\nAnalysis: {response}"
            else:
                # Fallback if LLM fails
                return f"Observation: {observation}\nAnalysis: Will proceed with the task."
        except Exception as e:
            # Fallback on error
            return f"Observation: {observation}\nAnalysis: Will proceed with the task."
    
    def reflect(self, action_result: Dict[str, Any]) -> str:
        """
        Reflect on the result of an action
        
        Args:
            action_result: Result from executing an action
            
        Returns:
            Reflection on the result
        """
        success = action_result.get('success', False)
        
        # If LLM is available, use it for enhanced reflection
        if self.llm_manager and self.llm_manager.is_enabled():
            reflection = self._llm_reflect(action_result)
        else:
            # Fallback to basic reflection
            if success:
                reflection = f"Action succeeded. Result: {action_result.get('result', 'N/A')}"
            else:
                error = action_result.get('error', 'Unknown error')
                reflection = f"Action failed. Error: {error}. Need to try a different approach."
        
        self.reflections.append(reflection)
        return reflection
    
    def _llm_reflect(self, action_result: Dict[str, Any]) -> str:
        """
        Use LLM for reflection on action results
        
        Args:
            action_result: Result from action
            
        Returns:
            LLM-generated reflection
        """
        success = action_result.get('success', False)
        result_str = str(action_result.get('result', 'N/A'))
        error_str = str(action_result.get('error', 'None'))
        
        prompt = f"""Reflect on this action result and provide a brief assessment (1-2 sentences).

Action Success: {success}
Result: {result_str}
Error: {error_str}

Provide a concise reflection on what happened and what it means."""

        try:
            response = self.llm_manager.generate(prompt, temperature=0.7, max_tokens=100)
            if response:
                return response
            else:
                # Fallback
                if success:
                    return f"Action succeeded. Result: {result_str}"
                else:
                    return f"Action failed. Error: {error_str}"
        except Exception as e:
            # Fallback on error
            if success:
                return f"Action succeeded. Result: {result_str}"
            else:
                return f"Action failed. Error: {error_str}"
    
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
