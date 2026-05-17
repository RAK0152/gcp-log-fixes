
from google.cloud import bigquery

def create_or_replace_table(project_id, dataset_id, table_id, schema, client=None):
    """
    Creates a BigQuery table, or replaces it if it already exists.
    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the dataset to create the table in.
        table_id (str): The ID of the table to create.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
        client (google.cloud.bigquery.Client, optional): BigQuery client. If not provided, a new one will be created.
    """
    if client is None:
        client = bigquery.Client(project=project_id)

    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        # Attempt to create the table. If it exists, an exception will be raised.
        table = client.create_table(table)
        print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created.")
    except Exception as e:
        if "Already Exists" in str(e):
            print(f"Table {project_id}.{dataset_id}.{table_id} already exists. Attempting to replace.")
            # If the table already exists, update it to replace its content and schema
            table = client.update_table(table, ["schema"])
            print(f"Table {table.project}.{table.dataset_id}.{table.table_id} replaced.")
        else:
            raise e

def create_table_if_not_exists(project_id, dataset_id, table_id, schema, client=None):
    """
    Creates a BigQuery table only if it does not already exist.
    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the dataset to create the table in.
        table_id (str): The ID of the table to create.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
        client (google.cloud.bigquery.Client, optional): BigQuery client. If not provided, a new one will be created.
    """
    if client is None:
        client = bigquery.Client(project=project_id)

    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)  # Check if table exists
        print(f"Table {project_id}.{dataset_id}.{table_id} already exists. Skipping creation.")
    except Exception as e:
        if "Not found" in str(e):
            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)
            print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created.")
        else:
            raise e


if __name__ == "__main__":
    # Example Usage:
    PROJECT_ID = "your-gcp-project-id"  # Replace with your project ID
    DATASET_ID = "your_dataset_id"  # Replace with your dataset ID
    TABLE_ID = "your_table_id"  # Replace with your table ID

    # Define a sample schema
    sample_schema = [
        bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]

    print("--- Demonstrating create_table_if_not_exists ---")
    create_table_if_not_exists(PROJECT_ID, DATASET_ID, TABLE_ID, sample_schema)

    # To demonstrate replacement, you might change the schema and call create_or_replace_table
    # print("\n--- Demonstrating create_or_replace_table (with potential schema change) ---")
    # updated_schema = [
    #     bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    #     bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    #     bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
    # ]
    # create_or_replace_table(PROJECT_ID, DATASET_ID, TABLE_ID, updated_schema)

    print("\nRemember to replace 'your-gcp-project-id', 'your_dataset_id', and 'your_table_id' with your actual values.")
    print("This script demonstrates two approaches: checking for existence or using replacement logic.")
