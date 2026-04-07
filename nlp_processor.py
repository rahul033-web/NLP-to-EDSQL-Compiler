import re

def process_query(query):
    """
    Parses natural language into a structured dictionary for the database.
    Optimized for SELECT, INSERT, UPDATE, DELETE, and AVERAGE.
    """
    query = query.lower().strip()

    data = {
        "action": None,
        "table": "students",
        "conditions": [],
        "values": {},      # For INSERT and Target detection
        "set_values": {},  # For UPDATE
        "logic": "AND"
    }

    # 1. ACTION DETECTION
    # Inside nlp_processor.py -> Action Detection
    if any(word in query for word in ["count", "total", "how many"]):
        data["action"] = "COUNT"
    elif any(word in query for word in ["average", "mean", "avg"]):
        data["action"] = "AVERAGE"
    elif any(word in query for word in ["show", "list", "get", "find", "search"]):
        data["action"] = "SELECT"
    elif any(word in query for word in ["add", "insert", "create", "new"]):
        data["action"] = "INSERT"
    elif any(word in query for word in ["delete", "remove", "drop", "wipe"]):
        data["action"] = "DELETE"
    elif any(word in query for word in ["update", "change", "set", "modify"]):
        data["action"] = "UPDATE"

    # 2. TARGET DETECTION (For Averages)
    if data["action"] == "AVERAGE":
        if "mark" in query: data["values"]["target"] = "marks"
        elif "age" in query: data["values"]["target"] = "age"
        else: data["values"]["target"] = "marks"

    # 3. OPERATOR MAPPING
    op_map = {
        "greater than": ">", "more than": ">", "above": ">", "older than": ">",
        "less than": "<", "below": "<", "under": "<", "younger than": "<",
        "equal to": "=", "equals": "=", "is": "=", "named": "=", "name": "=", "id": "="
    }

    # 4. UPDATE HANDLING (Extract NEW values)
    if data["action"] == "UPDATE":
        for col in ["name", "age", "marks"]:
            set_match = re.search(rf"{col}\s+(?:to\s+|set\s+)?([\w\d]+)", query)
            if set_match:
                data["set_values"][col] = set_match.group(1)
                query = query.replace(set_match.group(0), "PROCESSED")

    # 5. CONDITION EXTRACTION (The "Where" Clause - FIXES DELETE)
    # This regex is flexible to catch "id 11", "id is 11", "id: 11", or "named amit"
    columns = ["id", "name", "age", "marks"]
    for col in columns:
        # Check for operators first (e.g., "age > 20")
        for phrase, op in op_map.items():
            pattern = rf"\b{col}\b\s*(?:with|where|is|named|of)?\s*{phrase}\s+([\w\d]+)"
            match = re.search(pattern, query)
            if match:
                val = match.group(1).strip()
                if (col, op, val) not in data["conditions"]:
                    data["conditions"].append((col, op, val))
        
        # Fallback: Catch simple "column value" patterns like "id 11"
        if not any(c[0] == col for c in data["conditions"]):
            simple_pattern = rf"\b{col}\b\s+(?:is|at|:)?\s*([\w\d]+)"
            match = re.search(simple_pattern, query)
            if match:
                val = match.group(1).strip()
                # Ensure we aren't re-grabbing a value already used in an UPDATE set
                if col not in data["set_values"]:
                    data["conditions"].append((col, "=", val))

    # 6. INSERT LOGIC
    if data["action"] == "INSERT":
        name_match = re.search(r"(?:name|named|is)\s+([a-zA-Z]+)", query)
        age_match = re.search(r"age\s*(\d+)", query)
        marks_match = re.search(r"marks\s*(\d+)", query)
        if name_match: data["values"]["name"] = name_match.group(1).capitalize()
        if age_match: data["values"]["age"] = age_match.group(1)
        if marks_match: data["values"]["marks"] = marks_match.group(1)

    return data