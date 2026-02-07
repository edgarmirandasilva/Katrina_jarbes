"""
Calculator Skill - Performs mathematical calculations
"""

from typing import Dict, Any
from .base_skill import Skill
import ast
import operator


class CalculatorSkill(Skill):
    """Performs safe mathematical calculations"""
    
    def __init__(self):
        super().__init__()
        self.description = "Perform mathematical calculations safely"
        self.parameters = {
            'type': 'object',
            'properties': {
                'expression': {
                    'type': 'string',
                    'description': 'Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")'
                }
            },
            'required': ['expression']
        }
    
    def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """Execute a mathematical calculation"""
        try:
            # Safe evaluation of mathematical expressions
            result = self._safe_eval(expression)
            return {
                'success': True,
                'result': result,
                'expression': expression
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the skill schema"""
        return {
            'name': 'calculator',
            'description': self.description,
            'parameters': self.parameters
        }
    
    def _safe_eval(self, expr: str):
        """Safely evaluate a mathematical expression"""
        # Define allowed operations
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                return operators[type(node.op)](operand)
            else:
                raise ValueError(f"Unsupported operation: {type(node)}")
        
        try:
            tree = ast.parse(expr, mode='eval')
            return eval_node(tree.body)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
