
from google.cloud import bigquery
import time

def fix_bigquery_streaming_dml_error(project_id, dataset_id, table_id):
    """
    This function provides a solution to the BigQuery error:
    "UPDATE or DELETE statement over table ... would affect rows in the streaming buffer,
    which is not supported."

    The recommended approach is to use a MERGE statement, which is more robust
    when dealing with tables that receive streaming inserts. MERGE can safely
    update, insert, or delete rows in a table, even if it contains data in
    the streaming buffer, by operating on the stable base table.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the BigQuery dataset.
        table_id (str): The ID of the BigQuery table experiencing the error.
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Example: Create a temporary table as a source for the MERGE operation.
    # In a real-world scenario, this 'source' could be a subquery,
    # a temporary table, or another existing table containing the
    # changes you want to apply.
    source_table_id = f"{dataset_id}.temp_merge_source_{int(time.time())}"
    source_table_ref = client.dataset(dataset_id).table(source_table_id)

    try:
        # Ensure the target table exists before running MERGE
        try:
            client.get_table(table_ref) # This will raise an exception if the table does not exist
            print(f"Target table '{table_ref}' exists.")
        except Exception as e:
            print(f"Error: Target table '{table_ref}' does not exist or is inaccessible. Please ensure the table exists and you have permissions. Error: {e}")
            return

        # Create a dummy source table for demonstration
        # This source table will contain the data that you want to update/delete/insert
        # into your target_table.
        source_schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("status", "STRING"),
        ]
        source_table = bigquery.Table(source_table_ref, schema=source_schema)
        client.create_table(source_table, exists_ok=True)
        print(f"Created temporary source table: {source_table_ref}")

        # Insert some data into the source table (data to be merged)
        # This sample data assumes you want to update the row with id=1 and delete row with id=3.
        source_rows_to_insert = [
            {"id": 1, "name": "Alice Updated", "status": "active"},
            {"id": 3, "name": "Charlie to be Deleted", "status": "inactive"} # This row will cause deletion in target
        ]
        client.insert_rows_json(source_table_ref, source_rows_to_insert)
        print(f"Inserted sample data into source table: {source_table_ref}")
        # Give some time for streaming inserts to settle if this were a real scenario
        # In a real streaming scenario, you might have a delay or a separate process
        # that populates this source table with the 'resolved' data.
        time.sleep(5)

        # The MERGE statement to address the streaming buffer issue
        # This example assumes 'id' is the primary key for matching.
        # It deletes matched rows where source status is 'inactive',
        # updates matched rows otherwise, and can optionally insert non-matched rows.
        merge_query = f"""
        MERGE `{table_ref}` T
        USING `{source_table_ref}` S
        ON T.id = S.id
        WHEN MATCHED AND S.status = 'inactive' THEN
            DELETE
        WHEN MATCHED THEN
            UPDATE SET
                T.name = S.name,
                T.status = S.status
        -- WHEN NOT MATCHED BY TARGET THEN
        --     INSERT (id, name, status) VALUES (S.id, S.name, S.status)
        ;
        """

        print(f"
Executing MERGE statement on table: {table_ref}")
        print("Query:\n", merge_query)

        query_job = client.query(merge_query)
        query_job.result()  # Waits for the job to complete
        print(f"MERGE operation completed successfully for table: {table_ref}")
        print("This method is robust against streaming buffer issues because MERGE ")
        print("statements operate on the stable base table and handle eventual ")
        print("consistency with the streaming buffer gracefully, avoiding direct DML ")
        print("conflicts with buffered data.")

    except Exception as e:
        print(f"An error occurred during MERGE operation: {e}")
        raise
    finally:
        # Clean up the temporary source table
        try:
            client.delete_table(source_table_ref)
            print(f"Deleted temporary source table: {source_table_ref}")
        except Exception as e:
            print(f"Error cleaning up source table {source_table_ref}: {e}")

# Example usage (uncomment and replace with your actual project, dataset, and table details)
# if __name__ == "__main__":
#     # From the error message: ai-practice-388514.case_management.cases
#     PROJECT_ID = "ai-practice-388514"
#     DATASET_ID = "case_management"
#     TABLE_ID = "cases"
#     # Ensure the target table `ai-practice-388514.case_management.cases` exists
#     # and has at least 'id', 'name', 'status' columns or adjust schema/query accordingly.
#     fix_bigquery_streaming_dml_error(PROJECT_ID, DATASET_ID, TABLE_ID)
