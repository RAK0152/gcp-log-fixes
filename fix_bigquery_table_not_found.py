
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def fix_bigquery_table_not_found(project_id: str, dataset_id: str, table_id: str, location: str):
    """
    Checks if a BigQuery table exists and creates it if it does not.
    This fix provides a basic schema. You may need to adjust the schema
    according to your actual table requirements.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)  # API request
        print(f"Table {project_id}:{dataset_id}.{table_id} already exists.")
    except NotFound:
        print(f"Table {project_id}:{dataset_id}.{table_id} not found. Creating table...")
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("data", "STRING"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        table.location = location
        try:
            table = client.create_table(table)  # API request
            print(f"Table {table.project}:{table.dataset_id}.{table.table_id} created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    PROJECT_ID = "ai-practice-388514"
    DATASET_ID = "loan_applications"
    TABLE_ID = "historical_ratios"
    LOCATION = "US"

    fix_bigquery_table_not_found(PROJECT_ID, DATASET_ID, TABLE_ID, LOCATION)
