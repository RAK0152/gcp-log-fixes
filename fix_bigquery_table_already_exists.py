
from google.cloud import bigquery

def create_table_if_not_exists(project_id, dataset_id, table_id, schema):
    """Creates a BigQuery table if it does not already exist."""
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    table = bigquery.Table(table_ref, schema=schema)

    try:
        table = client.create_table(table, exists_ok=True)
        print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created or already existed.")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    # Replace with your project, dataset, and desired table details
    project_id = "your-gcp-project-id"  # e.g., "ai-practice-388514"
    dataset_id = "your_dataset_id"  # e.g., "sap_data"
    table_id = "your_table_id"  # e.g., "purchase_orders"

    # Define your table's schema
    table_schema = [
        bigquery.SchemaField("PurchaseOrder", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("PurchaseOrderType", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchaseOrderDate", "STRING", mode="NULLABLE"),
        # Add other fields as per your log analysis or actual schema
    ]

    create_table_if_not_exists(project_id, dataset_id, table_id, table_schema)
