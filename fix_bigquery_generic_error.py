
import google.cloud.bigquery

def run_bigquery_query(project_id, query):
    """Runs a BigQuery query and handles potential errors."""
    client = google.cloud.bigquery.Client(project=project_id)
    try:
        query_job = client.query(query)
        results = query_job.result()
        print("Query executed successfully.")
        for row in results:
            print(row)
        return results
    except Exception as e:
        print(f"An error occurred during BigQuery query execution: {e}")
        # In a real scenario, you might log the error, send an alert, or retry.
        return None

if __name__ == "__main__":
    # Replace with your GCP project ID and a sample query
    your_project_id = "your-gcp-project-id"
    sample_query = "SELECT 1"

    print(f"Attempting to run BigQuery query: {sample_query}")
    run_bigquery_query(your_project_id, sample_query)
