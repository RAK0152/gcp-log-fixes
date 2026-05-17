import google.cloud.bigquery as bq

client = bq.Client()

def create_table_if_not_exists(dataset_id, table_id, schema):
    """Create a BigQuery table only if it doesn't already exist."""
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists, skipping creation.")
    except Exception:
        table = bq.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Created table {table_id}")
