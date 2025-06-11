from dotenv import load_dotenv
import json
import os
from typing import Dict, Any

load_dotenv()

from src.crewai_prod.crew import ProductTaggingCrew
from memory_db import MemoryDB

def show_memory_insights(db: MemoryDB):
    """Show insights from memory to help users"""
    try:
        print("\n📊 Memory Insights:")
        
        # Show popular tags
        popular_tags = db.get_popular_tags(5)
        if popular_tags:
            print("🏷️  Most used tags:", ", ".join([f"{tag}({count})" for tag, count in popular_tags]))
        
        # Show recent history
        history = db.get_run_history(3)
        if history:
            print("\n📚 Recent runs:")
            for i, run in enumerate(history, 1):
                print(f"  {i}. {run['product']} → {run['persona'][:30]}...")
    except Exception as e:
        print(f"⚠️  Could not load memory insights: {e}")

def get_context_from_memory(db: MemoryDB, product: str, persona: str) -> str:
    """Generate context from similar past runs"""
    try:
        similar_runs = db.fetch_similar_runs(product, persona, 2)
        
        if not similar_runs:
            return ""
        
        context = "\n\n## Context from similar past runs:\n"
        for run in similar_runs:
            context += f"- Product: {run[0]}, Persona: {run[1]}\n"
            if run[2]:  # description
                context += f"  Description: {run[2][:100]}...\n"
            try:
                tags = json.loads(run[3]) if run[3] else []
                if tags:
                    context += f"  Tags: {', '.join(tags)}\n"
            except:
                pass
            context += "\n"
        
        return context
    except Exception as e:
        print(f"⚠️  Could not fetch memory context: {e}")
        return ""

def check_environment() -> bool:
    """Basic environment check"""
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("💡 Please check your .env file")
        return False
    
    required_files = [
        'src/crewai_prod/config/agents.yaml',
        'src/crewai_prod/config/tasks.yaml'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
    
    return True

def run():
    # Environment check
    if not check_environment():
        return
    
    # Initialize database
    try:
        db = MemoryDB()
    except Exception as e:
        print(f"❌ Could not initialize database: {e}")
        return
    
    try:
        # Show memory insights
        show_memory_insights(db)

        # Optional: Load previous input
        last_run = db.fetch_last_run()
        if last_run:
            print(f"\n🔎 Last run ({last_run[3]}):")
            print(f"Product: {last_run[0]}")
            print(f"Persona: {last_run[1]}")
            print("=" * 50)

        # Get user inputs (minimal validation here - let YAML handle detailed validation)
                # Get user inputs
        product = input("\nEnter product name: ").strip()
        persona = input("Enter persona description: ").strip()
        
        # Check cache first (exact match)
        cached_result = db.fetch_exact_run(product, persona)
        if cached_result:
            print("\n⚡ Using cached result from memory:")
            print(f"📝 Cached Output:\n{cached_result['output']}")
            return  # Exit since we found a cached run

        # If no cache found, continue to generate new result
        memory_context = get_context_from_memory(db, product, persona)

        inputs = {
            "product_name": product,
            "persona_description": persona,
            "memory_context": memory_context
        }

        print("\n🤖 Starting CrewAI agent...")

        result = ProductTaggingCrew().crew().kickoff(inputs=inputs)

        result_str = str(result)
        if "❌ ERROR:" in result_str:
            print(f"\n{result_str}")
            return

        print("\n✅ Task completed successfully!")
        print(f"\n📝 Result:\n{result}")

        output_str = json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else str(result)

        db.save_run(product, persona, output_str)
        print("✅ Output saved to memory db!")


    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        print("💡 Please check your configuration and try again")
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    run()