
from google.cloud import bigquery

def validate_bigquery_query(project_id: str, query: str) -> bool:
    """
    Validates a BigQuery SQL query without executing it.

    Args:
        project_id: Your Google Cloud project ID.
        query: The SQL query string to validate.

    Returns:
        True if the query is valid, False otherwise.
    """
    client = bigquery.Client(project=project_id)
    try:
        # Dry run the query to validate it
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        client.query(query, job_config=job_config)
        print(f"Query is valid:\n{query}")
        return True
    except Exception as e:
        print(f"Query is invalid:\n{query}\nError: {e}")
        return False

if __name__ == "__main__":
    # Replace with your project ID and a sample query
    PROJECT_ID = "your-gcp-project-id"
    VALID_QUERY = "SELECT * FROM `bigquery-public-data.usa_names.usa_1910_2013` LIMIT 10"
    INVALID_QUERY = "SELECT * FROM `non-existent-project.non_existent_dataset.non_existent_table` LIMIT 10"

    print("--- Validating a valid query ---")
    validate_bigquery_query(PROJECT_ID, VALID_QUERY)

    print("\n--- Validating an invalid query ---")
    validate_bigquery_query(PROJECT_ID, INVALID_QUERY)
