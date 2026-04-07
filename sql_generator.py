def generate_sql(data):
    """
    Translates the parsed NLP dictionary into a valid SQL string.
    This is used for display purposes in the UI 'Parsed Logic' section.
    """
    action = data.get("action")
    table = data.get("table", "students")
    logic = data.get("logic", "AND")
    
    if not action:
        return "-- Could not determine action (Try: Show, Add, Delete, Update) --"

    # 🔹 SELECT (Read)
    if action == "SELECT":
        sql = f"SELECT * FROM {table}"
        if data["conditions"]:
            conds = [f"{c} {o} '{v}'" if isinstance(v, str) and not v.isdigit() else f"{c} {o} {v}" 
                     for c, o, v in data["conditions"]]
            sql += " WHERE " + f" {logic} ".join(conds)
        return sql + ";"

    # 🔹 INSERT (Create)
    elif action == "INSERT":
        vals = data.get("values", {})
        if not vals:
            return "-- INSERT Error: No values provided (e.g., name, age) --"
            
        cols = ", ".join(vals.keys())
        formatted_vals = [f"'{v}'" if isinstance(v, str) and not v.isdigit() else str(v) 
                          for v in vals.values()]
        val_string = ", ".join(formatted_vals)
        
        return f"INSERT INTO {table} ({cols}) VALUES ({val_string});"

    # 🔹 DELETE (Destroy)
    elif action == "DELETE":
        sql = f"DELETE FROM {table}"
        if data["conditions"]:
            conds = [f"{c} {o} '{v}'" if isinstance(v, str) and not v.isdigit() else f"{c} {o} {v}" 
                     for c, o, v in data["conditions"]]
            sql += " WHERE " + f" {logic} ".join(conds)
            return sql + ";"
        return "-- DELETE Error: No conditions provided (Safety Lock) --"

    # 🔹 UPDATE (Edit)
    elif action == "UPDATE":
        if not data["set_values"]:
            return "-- UPDATE Error: No values to set (e.g., 'set marks 90') --"
            
        sql = f"UPDATE {table} SET "
        set_parts = [f"{k} = {v}" for k, v in data["set_values"].items()]
        sql += ", ".join(set_parts)

        if data["conditions"]:
            conds = [f"{c} {o} '{v}'" if isinstance(v, str) and not v.isdigit() else f"{c} {o} {v}" 
                     for c, o, v in data["conditions"]]
            sql += " WHERE " + f" {logic} ".join(conds)
        else:
            return "-- UPDATE Error: No condition provided (Safety Lock) --"
            
        return sql + ";"

    return "-- Invalid Logic Pattern --"