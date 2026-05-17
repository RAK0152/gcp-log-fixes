from google.cloud import bigquery
from google.api_core.exceptions import NotFound, Conflict

def create_bigquery_table_if_not_exists(project_id, dataset_id, table_id, schema_fields):
    """
    Checks if a BigQuery table exists and creates it if it does not.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the dataset.
        table_id (str): The ID of the table.
        schema_fields (list): A list of bigquery.SchemaField objects defining the table's schema.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)
        print(f"Table {project_id}.{dataset_id}.{table_id} already exists. Skipping creation.")
    except NotFound:
        print(f"Table {project_id}.{dataset_id}.{table_id} does not exist. Creating table...")
        table = bigquery.Table(table_ref, schema=schema_fields)
        try:
            table = client.create_table(table)
            print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created successfully.")
        except Conflict:
            # This can happen in a race condition where another process creates the table
            # between the get_table() and create_table() calls.
            print(f"Table {project_id}.{dataset_id}.{table_id} was just created by another process. Skipping creation.")
        except Exception as e:
            print(f"An unexpected error occurred during table creation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while checking for table existence: {e}")

# Example usage based on the first error log:
project_id_example = "ai-practice-388514"
dataset_id_example_1 = "sap_data"
table_id_example_1 = "purchase_orders"

# Define a sample schema based on the provided log entry for purchase_orders
# In a real scenario, this schema should be accurately defined from source.
schema_purchase_orders = [
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
    bigquery.SchemaField("DocumentCurrency", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ExchangeRate", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ExchangeRateIsFixed", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PaymentTerms", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("NetPaymentDays", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CashDiscount1Days", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CashDiscount1Percent", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CashDiscount2Days", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CashDiscount2Percent", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchasingProcessingStatus", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchasingCompletenessStatus", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ReleaseIsNotCompleted", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchasingDocumentOrigin", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchasingDocumentDeletionCode", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchaseOrderSubtype", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurchasingCollectiveNumber", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("SupplyingPlant", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("SupplyingSupplier", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("SupplierPhoneNumber", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("SupplierRespSalesPersonName", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("SupplierQuotationExternalID", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ManualSupplierAddressID", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("IsEndOfPurposeBlocked", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressName", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressCityName", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressStreetName", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressHouseNumber", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressPostalCode", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressRegion", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressCountry", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressPhoneNumber", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressFaxNumber", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AddressCorrespondenceLanguage", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Language", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("IncotermsClassification", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("IncotermsVersion", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("IncotermsLocation1", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("IncotermsLocation2", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ValidityStartDate", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ValidityEndDate", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CorrespncExternalReference", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("CorrespncInternalReference", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurgAggrgdSftyDataSheetStatus", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurgAggrgdProdMarketabilitySts", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurgAggrgdProdCmplncSuplrSts", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("PurgProdCmplncTotDngrsGoodsSts", "STRING", mode="NULLABLE")
]

# Example usage for the second type of error (lb_mtg_demo table)
dataset_id_example_2 = "lb_mtg_demo_us_central1_US"
table_id_example_2 = "895fc927-d21b-4e3e-ba4c-6e4a376d894e"

schema_lb_mtg_demo = [
    bigquery.SchemaField("project_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("location", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("app_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("app_version_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("conversation_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("turn_index", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("create_time", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("messages", "RECORD", mode="REPEATED",
        fields=[
            bigquery.SchemaField("role", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("event_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("chunks", "JSON", mode="NULLABLE"),
        ]),
    bigquery.SchemaField("root_spans", "RECORD", mode="REPEATED",
        fields=[
            bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("start_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("end_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("attributes", "JSON", mode="NULLABLE"),
            bigquery.SchemaField("child_spans", "JSON", mode="NULLABLE"),
        ]),
]

if __name__ == "__main__":
    print("Attempting to create/check 'sap_data.purchase_orders' table...")
    create_bigquery_table_if_not_exists(project_id_example, dataset_id_example_1, table_id_example_1, schema_purchase_orders)
    print("\nAttempting to create/check 'lb_mtg_demo_us_central1_US.895fc927-d21b-4e3e-ba4c-6e4a376d894e' table...")
    create_bigquery_table_if_not_exists(project_id_example, dataset_id_example_2, table_id_example_2, schema_lb_mtg_demo)
