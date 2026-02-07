"""
Example: Basic Agent Usage
Demonstrates how to use the Katrina agent with various skills
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agent import Agent


def main():
    """Run basic agent examples"""
    
    print("="*60)
    print("🤖 Katrina Agent - Basic Example")
    print("="*60)
    
    # Initialize agent
    agent = Agent(name="Katrina", memory_dir="./memory_store")
    
    # Example 1: Calculator skill
    print("\n📊 Example 1: Calculator")
    response = agent.process("calculate 25 + 17")
    print(f"Response: {response}")
    
    # Example 2: File operations
    print("\n📁 Example 2: File Operations")
    
    # Write a file
    response = agent.process("write Hello World to test.txt")
    print(f"Response: {response}")
    
    # List files
    response = agent.process("list files")
    print(f"Response: {response}")
    
    # Read file
    response = agent.process("read test.txt")
    print(f"Response: {response}")
    
    # Example 3: Memory search
    print("\n🔍 Example 3: Memory Search")
    response = agent.process("search for calculator")
    print(f"Response: {response}")
    
    # Example 4: Help
    print("\n❓ Example 4: Help")
    response = agent.process("help")
    print(f"Response: {response}")
    
    # Show agent status
    print("\n📈 Agent Status:")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Examples completed!")


if __name__ == "__main__":
    main()
