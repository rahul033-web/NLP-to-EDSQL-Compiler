import pandas as pd
import os

# Define the absolute path for the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "students.csv")

def create_database():
    """Initializes the CSV with 10 entries if it doesn't exist."""
    if not os.path.exists(csv_path):
        data = {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "name": ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Rahul"],
            "age": [20, 19, 22, 21, 23, 20, 24, 22, 19, 21],
            "marks": [85, 92, 78, 95, 88, 72, 65, 90, 81, 85]
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        print(f"✅ Created initial database at {csv_path}")

def execute_query(data):
    """Executes the parsed NLP logic against the Pandas DataFrame."""
    try:
        if not os.path.exists(csv_path):
            return [["Error", "Database file (CSV) not found.", "-", "-"]]

        df = pd.read_csv(csv_path)
        action = data.get("action")

        # --- 1. SELECT (Read / Filter) ---
        if action == "SELECT":
            results = df.copy()
            for col, op, val in data.get("conditions", []):
                if str(val).isdigit():
                    # Force column to numeric so '19 < 21' is math, not text
                    results[col] = pd.to_numeric(results[col], errors='coerce')
                    val = int(val)
                    if op == ">": results = results[results[col] > val]
                    elif op == "<": results = results[results[col] < val]
                    elif op == "=": results = results[results[col] == val]
                else:
                    # Case-insensitive name search
                    results = results[results[col].astype(str).str.lower() == str(val).lower()]
            
            if results.empty:
                return [["No Results", "No students matched your filter", "-", "-"]]
            return results.values.tolist()
        
    
     # --- 📊 POSITION-AWARE AVERAGE LOGIC ---
        elif action == "AVERAGE":
            target_col = data.get("values", {}).get("target", "marks")
            
            if target_col in df.columns:
                df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
                avg_val = round(df[target_col].mean(), 2)
                
                # If we are averaging MARKS, put the value in the 4th spot
                if target_col == "marks":
                    return [["Result", "The average marks is:", "-", avg_val]]
                
                # If we are averaging AGE, put the value in the 3rd spot
                else:
                    return [["Result", "The average age is:", avg_val, "-"]]
            
            return [["Error", "Column not found", "-", "-"]]
        
        # --- 🔢 COUNT LOGIC ---
    
        elif action == "COUNT":
            # 1. Start with a copy of the full table
            results = df.copy()
            
            # 2. Apply any conditions (e.g., "count students where marks > 80")
            for col, op, val in data.get("conditions", []):
                # Ensure the column exists before filtering
                if col in results.columns:
                    if str(val).isdigit():
                        results[col] = pd.to_numeric(results[col], errors='coerce')
                        val = int(val)
                        if op == ">": results = results[results[col] > val]
                        elif op == "<": results = results[results[col] < val]
                        elif op == "=": results = results[results[col] == val]
                    else:
                        # String matching for names
                        results = results[results[col].astype(str).str.lower() == str(val).lower()]
            
            # 3. Calculate the total
            total_count = len(results)
            
            # 4. Return exactly 5 items to match the HTML headers:
            # [ID, NAME, AGE, MARKS, COUNT]
            # We put the number in the 5th spot (index 4)
            return [["-", "Total Records Found", "-", "-", total_count]]
        
        # --- 2. INSERT (Create) ---
        elif action == "INSERT":
            vals = data.get("values", {})
            # Check for manual ID insertion (filling gaps)
            specific_id = next((int(v) for c, o, v in data.get("conditions", []) if c == "id"), None)
            
            if specific_id and specific_id in df["id"].values:
                return [["Error", f"ID {specific_id} already exists.", "-", "-"]]
            
            new_id = specific_id if specific_id else (int(df["id"].max() + 1) if not df.empty else 1)
            
            new_row = {
                "id": new_id,
                "name": vals.get("name", "New Student"),
                "age": int(vals.get("age", 0)),
                "marks": int(vals.get("marks", 0))
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df = df.sort_values(by="id").to_csv(csv_path, index=False)
            return [["Success", f"Added {new_row['name']} at ID {new_id}", "-", "-"]]

        # --- 3. UPDATE (Modify) ---
        elif action == "UPDATE":
            if not data.get("conditions") or not data.get("set_values"):
                return [["Error", "Target ID and New Value required.", "-", "-"]]

            mask = pd.Series([True] * len(df))
            for col, op, val in data["conditions"]:
                df[col] = pd.to_numeric(df[col], errors='coerce') if str(val).isdigit() else df[col]
                mask &= (df[col] == int(val)) if str(val).isdigit() else (df[col].astype(str).str.lower() == str(val).lower())

            if mask.any():
                for col, val in data["set_values"].items():
                    df.loc[mask, col] = int(val) if str(val).isdigit() else val
                df.to_csv(csv_path, index=False)
                return [["Success", "Record updated.", "-", "-"]]
            return [["Error", "Student not found.", "-", "-"]]

        # --- 4. DELETE (Remove) ---
        elif action == "DELETE":
            original_len = len(df)
            for col, op, val in data.get("conditions", []):
                if str(val).isdigit():
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    val = int(val)
                    if op == "=": df = df[df[col] != val]
                else:
                    df = df[df[col].astype(str).str.lower() != str(val).lower()]
            
            if len(df) < original_len:
                df.to_csv(csv_path, index=False)
                return [["Success", "Deleted record.", "-", "-"]]
            return [["Info", "Nothing to delete.", "-", "-"]]

    except Exception as e:
        return [[f"System Error: {str(e)}", "-", "-", "-"]]
    
            

    return []