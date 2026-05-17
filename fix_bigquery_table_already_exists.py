from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def fix_bigquery_table_already_exists(project_id, dataset_id, table_id, schema):
    """
    Checks if a BigQuery table exists, and creates it if it does not.
    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): Your BigQuery dataset ID.
        table_id (str): Your BigQuery table ID.
        schema (list): The schema of the table to be created, e.g.,
                       [bigquery.SchemaField("column_name", "STRING", mode="NULLABLE")].
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)
        print(f"Table {project_id}.{dataset_id}.{table_id} already exists. No action needed.")
    except NotFound:
        print(f"Table {project_id}.{dataset_id}.{table_id} does not exist. Creating table...")
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table {project_id}.{dataset_id}.{table_id} created successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage based on the provided log error:
# This example extracts the project, dataset, table, and schema from the log.
if __name__ == "__main__":
    project_id = "ai-practice-388514"
    dataset_id = "sap_data"
    table_id = "purchase_orders"

    # Schema extracted from the log entry
    schema = [
        bigquery.SchemaField("PurchaseOrder", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("PurchaseOrderType", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchaseOrderDate", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CreationDate", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("LastChangeDateTime", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CreatedByUser", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("CompanyCode", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Supplier", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("InvoicingParty", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchasingOrganization", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchasingGroup", "STRING", mode="NULLABLE"),
        # Note: The log entry was truncated. If there are more fields,
        # they should be added here. This example assumes the provided part is complete
        # or demonstrates how to add them.
    ]

    fix_bigquery_table_already_exists(project_id, dataset_id, table_id, schema)
