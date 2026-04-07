from flask import Flask, render_template, request
from nlp_processor import process_query
from database import create_database, execute_query
import os

app = Flask(__name__)

# 1. Initialize the CSV with 10 entries on startup
create_database()

def generate_sql_display(data):
    """
    Translates the NLP dictionary into a readable SQL string 
    specifically for the 'Parsed Logic' box in the UI.
    """
    action = data.get("action")
    table = data.get("table", "students")
    conditions = data.get("conditions", [])
    
    if action == "SELECT":
        sql = f"SELECT * FROM {table}"
        if conditions:
            cond_str = " AND ".join([f"{c[0]} {c[1]} '{c[2]}'" for c in conditions])
            sql += f" WHERE {cond_str}"
        return sql + ";"

    elif action == "AVERAGE":
        target = data.get("values", {}).get("target", "marks")
        return f"SELECT AVG({target}) FROM {table};"
    
    # Inside generate_sql_display in app.py
    elif action == "COUNT":
        sql = f"SELECT COUNT(*) FROM {table}"
        if conditions:
            cond_str = " AND ".join([f"{c[0]} {c[1]} '{c[2]}'" for c in conditions])
            sql += f" WHERE {cond_str}"
        return sql + ";"

    elif action == "INSERT":
        vals = data.get("values", {})
        # Check if a specific ID was requested in conditions
        spec_id = next((c[2] for c in conditions if c[0] == 'id'), None)
        
        cols = list(vals.keys())
        values = [f"'{v}'" for v in vals.values()]
        
        if spec_id:
            cols.insert(0, "id")
            values.insert(0, f"'{spec_id}'")
            
        return f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(values)});"

    elif action == "UPDATE":
        set_vals = data.get("set_values", {})
        set_str = ", ".join([f"{k}='{v}'" for k, v in set_vals.items()])
        where_str = " AND ".join([f"{c[0]}{c[1]}'{c[2]}'" for c in conditions])
        return f"UPDATE {table} SET {set_str} WHERE {where_str};"

    elif action == "DELETE":
        if not conditions:
            return "-- DELETE Error: Safety Lock (No condition) --"
        where_str = " AND ".join([f"{c[0]}{c[1]}'{c[2]}'" for c in conditions])
        return f"DELETE FROM {table} WHERE {where_str};"

    return "-- Pending valid query --"

@app.route("/", methods=["GET", "POST"])
def home(): 
    display_sql = ""
    result = []
    user_query = ""

    if request.method == "POST":
        # Get the natural language from the user
        user_query = request.form.get("query", "").strip()

        if user_query:
            # 2. Convert text to a structured data dictionary
            data = process_query(user_query)
            
            # 3. Generate the SQL string for the "Parsed Logic" box
            display_sql = generate_sql_display(data)
            
            # 4. Execute the actual Pandas/CSV logic and get results
            result = execute_query(data)

    return render_template("index.html", sql=display_sql, result=result, query=user_query)

if __name__ == "__main__":
    app.run(debug=True, port=5000)