
from google.cloud import bigquery

def create_or_replace_bigquery_table(project_id, dataset_id, table_id, schema):
    """
    Creates a new BigQuery table or replaces an existing one if it already exists.
    This function addresses the "Already Exists: Table" error by using
    CREATE OR REPLACE TABLE functionality.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the dataset.
        table_id (str): The ID of the table to create or replace.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    # Construct a full table ID for logging
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    try:
        # Check if the table exists first (optional, but good for explicit logging)
        client.get_table(table_ref)
        print(f"Table {full_table_id} already exists. Attempting to replace.")
        # To replace an existing table, you would typically drop it and recreate it
        # or use a DDL statement like CREATE OR REPLACE TABLE in a query job.
        # For this example, we'll demonstrate a simple replacement strategy
        # by deleting and then creating. For large tables, consider ALTER TABLE or
        # external data loading options with WRITE_TRUNCATE.
        client.delete_table(table_ref, not_found_ok=True)
        print(f"Existing table {full_table_id} deleted.")
    except Exception as e:
        # If the table does not exist, get_table will raise an exception,
        # which is expected for a new table creation. We proceed to create.
        # For other exceptions, re-raise.
        if "Not found" not in str(e):
            raise
        print(f"Table {full_table_id} does not exist. Creating a new table.")

    # Define the table object with the schema
    table = bigquery.Table(table_ref, schema=schema)

    # Create the table (or recreate if it was deleted)
    table = client.create_table(table)
    print(f"Table {full_table_id} successfully created or replaced.")


# Example Usage (replace with your actual project, dataset, table, and schema)
if __name__ == "__main__":
    your_project_id = "ai-practice-388514"  # Replace with your project ID
    your_dataset_id = "sap_data"          # Replace with your dataset ID
    your_table_id = "purchase_orders"     # Replace with your table ID

    # Example schema, adapt to your actual table schema
    your_schema = [
        bigquery.SchemaField("PurchaseOrder", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("PurchaseOrderType", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("PurchaseOrderDate", "STRING", mode="NULLABLE"),
        # Add all other fields as per your table definition in the logs
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
        bigquery.SchemaField("PurgProdCmplncTotDngrsGoodsSts", "STRING", mode="NULLABLE"),
    ]

    create_or_replace_bigquery_table(your_project_id, your_dataset_id, your_table_id, your_schema)
