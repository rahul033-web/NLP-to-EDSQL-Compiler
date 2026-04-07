from nlp_processor import process_query
from database import create_database, execute_query
import pandas as pd

def main():
    print("---   NLP Compiler (CLI Mode) ---")
    
    # Ensure the 10 data entries exist in students.csv
    create_database()

    while True:
        print("\n" + "="*40)
        query = input("Enter Query (e.g., 'show students age > 20' or 'exit'): ").strip()

        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting Compiler. Goodbye!")
            break

        if not query:
            continue

        # 1. Process text into structured data
        data = process_query(query)
        
        print(f"\n🔍 [AI Understanding]:")
        print(f"   Action: {data['action']}")
        print(f"   Conditions: {data['conditions']}")

        # 2. Execute the logic against the CSV
        results = execute_query(data)

        # 3. Display Results
        print("\n📄 [Query Results]:")
        if not results:
            print("   (No records found or empty result)")
        else:
            # Simple column header for CLI
            print(f"{'ID':<5} | {'Name':<12} | {'Age':<5} | {'Marks':<5}")
            print("-" * 40)
            for r in results:
                # Handle both list data and success message strings
                if isinstance(r, list):
                    print(f"{r[0]:<5} | {r[1]:<12} | {r[2]:<5} | {r[3]:<5}")
                else:
                    print(f"   ✨ {r}")

if __name__ == "__main__":
    main()