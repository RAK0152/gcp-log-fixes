
from google.cloud import bigquery
from google.api_core.exceptions import Conflict

def create_bigquery_table_if_not_exists(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema: list[bigquery.SchemaField]
):
    """
    Creates a BigQuery table if it does not already exist.
    Uses exists_ok=True to prevent errors if the table already exists.
    """
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    table = bigquery.Table(table_ref, schema=schema)

    try:
        # Using exists_ok=True will prevent a Conflict error if the table already exists.
        table = client.create_table(table, exists_ok=True)
        print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created or already existed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage: Replace with your actual project, dataset, table, and schema
    your_project_id = "your-gcp-project-id"
    your_dataset_id = "your_dataset_name"
    your_table_id = "your_table_name"
    your_schema = [
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]

    print(f"Attempting to create table {your_project_id}:{your_dataset_id}.{your_table_id}...")
    create_bigquery_table_if_not_exists(your_project_id, your_dataset_id, your_table_id, your_schema)
