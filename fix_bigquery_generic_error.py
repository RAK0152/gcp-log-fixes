
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError

def run_bigquery_query_with_error_handling(project_id, query):
    """
    Runs a BigQuery query and handles potential errors.
    Args:
        project_id (str): Your Google Cloud project ID.
        query (str): The SQL query string.
    Returns:
        list: Query results if successful, None otherwise.
    """
    client = bigquery.Client(project=project_id)

    try:
        query_job = client.query(query)
        results = query_job.result()  # Waits for the job to complete.
        
        print("Query successful!")
        rows = []
        for row in results:
            rows.append(dict(row))
        return rows
    except GoogleAPIError as e:
        print(f"An error occurred during BigQuery query execution: {e}")
        # You can add more specific error handling here based on error codes or messages.
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace with your project ID and a sample query that might fail or succeed
    your_project_id = "your-gcp-project-id"
    
    # Example of a valid query
    valid_query = """
    SELECT
        name, SUM(number) as total_people
    FROM
        `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE
        state = 'TX'
    GROUP BY
        name
    ORDER BY
        total_people DESC
    LIMIT 10
    """

    # Example of an invalid query (e.g., syntax error, non-existent table)
    invalid_query = """
    SELECT non_existent_column
    FROM `bigquery-public-data.usa_names.non_existent_table`
    LIMIT 10
    """
    
    print("--- Running Valid Query ---")
    valid_results = run_bigquery_query_with_error_handling(your_project_id, valid_query)
    if valid_results:
        print(f"First 5 results: {valid_results[:5]}")

    print("\n--- Running Invalid Query ---")
    invalid_results = run_bigquery_query_with_error_handling(your_project_id, invalid_query)
    if invalid_results:
        print("This should not be printed for an invalid query.")
