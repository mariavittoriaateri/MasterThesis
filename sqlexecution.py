import sqlite3
import argparse

def execute_queries(database, query_file, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Read the SQL queries from the input file
    with open(query_file, 'r') as qf:
        queries = qf.readlines()

    # Open the output file for writing results
    with open(output_file, 'w') as of:
        for query in queries:
            query = query.strip()
            if not query:
                continue
            
            # Ensure query ends with a semicolon
            if not query.endswith(';'):
                query += ';'
            
            # Execute each query
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Write the results to the output file
                of.write(f"Results for query: {query}\n")
                if results:
                    for row in results:
                        of.write(f"{row}\n")
                else:
                    of.write("Nothing returned\n")
                of.write("\n")
            except sqlite3.Error as e:
                of.write(f"Error executing query: {query}\n")
                of.write(f"Error message: {e}\n\n")

    # Close the connection to the database
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute SQL queries from a file against a SQLite database and output the results to a file.")
    parser.add_argument("database", type=str, help="Path to the SQLite database file.")
    parser.add_argument("query_file", type=str, help="Path to the file containing SQL queries (one per line).")
    parser.add_argument("output_file", type=str, help="Path to the output file where results will be written.")

    args = parser.parse_args()
    execute_queries(args.database, args.query_file, args.output_file)
