"""
Example: Interactive Agent
Run an interactive conversation with the agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agent import Agent


def main():
    """Run interactive agent session"""
    
    print("="*60)
    print("🤖 Katrina Agent - Interactive Mode")
    print("="*60)
    print("Type 'help' for available commands")
    print("Type 'exit' or 'quit' to end the session")
    print("Type 'status' to see agent status")
    print("Type 'reset' to clear short-term memory")
    print("="*60)
    
    # Initialize agent
    agent = Agent(name="Katrina", memory_dir="./memory_store")
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break
            
            elif user_input.lower() == 'status':
                status = agent.get_status()
                print("\n📈 Agent Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
                continue
            
            elif user_input.lower() == 'reset':
                agent.reset()
                print("🔄 Agent memory reset")
                continue
            
            # Process input through agent
            response = agent.process(user_input, verbose=False)
            print(f"\n🤖 {agent.name}: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
