
from google.cloud import bigquery
from google.cloud.exceptions import Conflict

def create_bigquery_table_if_not_exists(project_id, dataset_id, table_id, schema):
    """
    Creates a BigQuery table if it does not already exist.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the dataset to create the table in.
        table_id (str): The ID of the table to create.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        table = client.create_table(table)  # Make an API request.
        print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created.")
    except Conflict:
        print(f"Table {project_id}.{dataset_id}.{table_id} already exists. Skipping creation.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage (replace with your actual project, dataset, table, and schema)
    PROJECT_ID = "ai-practice-388514"  # Replace with your project ID
    DATASET_ID = "sap_data"         # Replace with your dataset ID
    TABLE_ID = "purchase_orders"    # Replace with your table ID

    # Define your table schema based on the error message's schema snippet
    # Note: This is a simplified schema, adapt to your full schema
    SCHEMA = [
        bigquery.SchemaField("PurchaseOrder", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("PurchaseOrderType", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchaseOrderDate", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CreationDate", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("LastChangeDateTime", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CreatedByUser", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CompanyCode", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Supplier", "STRING", mode="NULLABLE"),
        # Add other fields as per your actual table schema
    ]

    create_bigquery_table_if_not_exists(PROJECT_ID, DATASET_ID, TABLE_ID, SCHEMA)
