import sqlite3

# Connect to database (creates if doesn't exist)
db = sqlite3.connect("school.db")
c = db.cursor()

# Read and execute SQL script from file
with open("sql_script.sql") as f:
    sql_script = f.read()

    # Split script by semicolons to get individual statements
    statements = sql_script.split(";")

    for statement in statements:
        # Skip empty statements (e.g., trailing semicolon)
        if statement.strip():
            try:
                # Execute statement
                result = c.execute(statement)

                # Use walrus operator to check if result has data to fetch
                # Only SELECT statements return fetchable results
                if fetch_result := result.fetchall():
                    print(fetch_result)
            except sqlite3.OperationalError:
                # Handle DDL statements (CREATE, DROP) that don't return results
                # and other SQL errors
                print(
                    f"Executed: {statement[:50]}..."
                )  # Print first 50 chars for debugging

# Commit changes to database
db.commit()

# Close database connection
db.close()
