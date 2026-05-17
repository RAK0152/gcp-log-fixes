
from google.cloud import bigquery

def validate_bigquery_query(project_id: str, query: str, location: str = "US") -> bool:
    """
    Validates a BigQuery SQL query by performing a dry run.

    Args:
        project_id: Your Google Cloud project ID.
        query: The SQL query string to validate.
        location: The geographic location of the BigQuery job (e.g., "US", "EU").

    Returns:
        True if the query is valid, False otherwise.
    """
    client = bigquery.Client(project=project_id, location=location)

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    try:
        query_job = client.query(query, job_config=job_config)
        print(f"Query validated successfully. This query will process {query_job.total_bytes_processed} bytes.")
        return True
    except Exception as e:
        print(f"Query validation failed: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    # Replace with your actual project ID and a query to test
    your_project_id = "your-gcp-project-id"
    valid_query = "SELECT COUNT(*) FROM `bigquery-public-data.usa_names.usa_1910_2013`"
    invalid_query = "SELECT * FROM `non_existent_dataset.non_existent_table`"

    print("\n--- Testing valid query ---")
    is_valid = validate_bigquery_query(your_project_id, valid_query)
    print(f"Is valid: {is_valid}")

    print("\n--- Testing invalid query ---")
    is_invalid = validate_bigquery_query(your_project_id, invalid_query)
    print(f"Is valid: {is_invalid}")
