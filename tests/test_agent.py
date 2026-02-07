"""
Simple tests to validate core agent functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agent import Agent
from src.skills import CalculatorSkill, FileOperationsSkill
from src.memory import MemoryManager


def test_calculator_skill():
    """Test calculator skill"""
    print("Testing Calculator Skill...")
    skill = CalculatorSkill()
    
    # Test addition
    result = skill.execute(expression="5 + 3")
    assert result['success']
    assert result['result'] == 8
    
    # Test multiplication
    result = skill.execute(expression="10 * 5")
    assert result['success']
    assert result['result'] == 50
    
    print("✅ Calculator skill tests passed")


def test_memory_manager():
    """Test memory manager"""
    print("Testing Memory Manager...")
    memory = MemoryManager(storage_dir="./test_memory", max_short_term=10)
    
    # Test storing interaction
    memory.add_interaction("Hello", "Hi there")
    
    # Test storing knowledge
    mem_id = memory.store_knowledge("Python is a programming language")
    assert mem_id is not None
    
    # Test search
    results = memory.search_long_term_memory("Python")
    assert len(results) > 0
    
    print("✅ Memory manager tests passed")


def test_agent_processing():
    """Test agent processing"""
    print("Testing Agent Processing...")
    agent = Agent(name="TestAgent", memory_dir="./test_memory")
    
    # Test calculator
    response = agent.process("calculate 10 + 5", verbose=False)
    assert "15" in response
    
    # Test help
    response = agent.process("help", verbose=False)
    assert "Katrina" in response or "TestAgent" in response
    
    # Test file operations
    response = agent.process("write test content to test_file.txt", verbose=False)
    assert "success" in response.lower() or "wrote" in response.lower()
    
    print("✅ Agent processing tests passed")


def test_nlp_processor():
    """Test NLP processor"""
    print("Testing NLP Processor...")
    from src.agent import NaturalLanguageProcessor
    
    nlp = NaturalLanguageProcessor()
    
    # Test calculator intent
    result = nlp.parse("calculate 5 + 3")
    assert result['intent'] == 'calculate'
    assert 'expression' in result['entities']
    
    # Test file read intent
    result = nlp.parse("read file notes.txt")
    assert result['intent'] == 'file_read'
    assert 'filename' in result['entities']
    
    # Test help intent
    result = nlp.parse("help")
    assert result['intent'] == 'help'
    
    print("✅ NLP processor tests passed")


def test_reasoning_engine():
    """Test reasoning engine"""
    print("Testing Reasoning Engine...")
    from src.agent import ReasoningEngine
    
    reasoning = ReasoningEngine()
    
    # Test thinking
    thought = reasoning.think("Need to calculate something")
    assert len(thought) > 0
    
    # Test reflection
    reflection = reasoning.reflect({'success': True, 'result': 42})
    assert "succeed" in reflection.lower()
    
    # Test planning
    plan = reasoning.plan("Calculate sum", ["calculator"])
    assert len(plan) > 0
    
    print("✅ Reasoning engine tests passed")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Running Agent Tests")
    print("="*60)
    
    try:
        test_calculator_skill()
        test_memory_manager()
        test_nlp_processor()
        test_reasoning_engine()
        test_agent_processing()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
