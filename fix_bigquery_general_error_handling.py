
from google.cloud import bigquery
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_bigquery_query(project_id: str, query: str):
    """
    Executes a BigQuery query and handles potential errors.
    """
    client = bigquery.Client(project=project_id)
    try:
        logging.info(f"Attempting to run query: {query}")
        query_job = client.query(query)  # API request
        results = query_job.result()  # Waits for job to complete.
        logging.info("Query executed successfully.")
        for row in results:
            logging.debug(row) # Log rows if needed for debugging
        return results
    except Exception as e:
        logging.error(f"An error occurred during BigQuery query execution: {e}")
        # Here you might add more specific error handling based on error type
        # For example, checking e.code or e.errors for BigQuery specific errors
        raise

def main():
    # Example usage:
    # Replace with your project ID and a sample query
    your_project_id = "your-gcp-project-id"
    sample_query = "SELECT 1" # Replace with a meaningful query that might fail

    try:
        logging.info("Starting BigQuery error handling demonstration.")
        # This will succeed
        run_bigquery_query(your_project_id, "SELECT 'Hello World' as greeting")

        # This will intentionally cause an error if the table does not exist
        # Uncomment to test error handling
        # run_bigquery_query(your_project_id, "SELECT * FROM `non_existent_dataset.non_existent_table`")

    except Exception as e:
        logging.critical(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()
