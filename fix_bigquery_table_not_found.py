
from google.cloud import bigquery

def create_bigquery_table_if_not_exists(project_id, dataset_id, table_id, schema, location="US"):
    """
    Creates a BigQuery table if it does not already exist.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): Your BigQuery dataset ID.
        table_id (str): Your BigQuery table ID.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
        location (str): The geographic location where the dataset should reside.
    """
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists in {dataset_id}.")
    except Exception as e:
        if "Not found" in str(e):
            print(f"Table {table_id} not found. Creating table...")
            table = bigquery.Table(table_ref, schema=schema)
            table.location = location  # Set the table location
            table = client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id} in location {table.location}")
        else:
            raise e

# Example Usage (replace with actual project, dataset, table details and schema)
PROJECT_ID = "ai-practice-388514"
DATASET_ID = "loan_applications"
TABLE_ID = "historical_ratios"
# Based on the failing query: SELECT DSCR, ICR, Debt_Equity, Current_Ratio, EBITDA_Margin
SCHEMA = [
    bigquery.SchemaField("DSCR", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("ICR", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Debt_Equity", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Current_Ratio", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("EBITDA_Margin", "FLOAT", mode="NULLABLE"),
    # Add other fields as per the actual table schema
]

# Uncomment the following line to run the fix
# create_bigquery_table_if_not_exists(PROJECT_ID, DATASET_ID, TABLE_ID, SCHEMA, location="US")
