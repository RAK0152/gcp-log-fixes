
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError

def execute_bigquery_query(project_id: str, query: str):
    """
    Executes a BigQuery SQL query and handles common errors.

    Args:
        project_id: Your Google Cloud project ID.
        query: The SQL query string to execute.

    Returns:
        A list of rows if the query is successful, None otherwise.
    """
    client = bigquery.Client(project=project_id)
    try:
        query_job = client.query(query)
        rows = list(query_job.result())
        print(f"Query executed successfully. Found {len(rows)} rows.")
        return rows
    except GoogleAPICallError as e:
        print(f"An error occurred during query execution: {e}")
        # You can add more specific error handling here based on error codes or messages
        if "Bad request" in str(e) or "Syntax error" in str(e):
            print("Likely a SQL syntax error or invalid query structure.")
        elif "Not found" in str(e):
            print("Table or dataset not found. Check your references.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace with your project ID and a sample problematic query
    # Example 1: Valid query
    print("--- Running a valid query ---")
    project = "your-gcp-project-id" # !!! IMPORTANT: Replace with your actual project ID
    valid_query = "SELECT 1 as example_column;"
    execute_bigquery_query(project, valid_query)

    # Example 2: Invalid query (syntax error)
    print("\n--- Running an invalid query (syntax error) ---")
    invalid_syntax_query = "SELECT FROM example_table;"
    execute_bigquery_query(project, invalid_syntax_query)

    # Example 3: Non-existent table query
    print("\n--- Running a query on a non-existent table ---")
    non_existent_table_query = f"SELECT * FROM `{project}.non_existent_dataset.non_existent_table`;"
    execute_bigquery_query(project, non_existent_table_query)
