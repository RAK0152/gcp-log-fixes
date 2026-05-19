from google.cloud import bigquery

def fix_streaming_update_issue(project_id: str, dataset_id: str, main_table_id: str, staging_table_id: str):
    """
    Addresses the BigQuery error: "UPDATE or DELETE statement over table ...
    would affect rows in the streaming buffer, which is not supported."

    This function executes a MERGE statement to apply changes from a staging table
    to the main table. This is a common pattern to avoid direct UPDATE/DELETE
    on tables with active streaming inserts, as MERGE operates on committed data.

    Args:
        project_id: The GCP project ID.
        dataset_id: The ID of the dataset containing the tables.
        main_table_id: The ID of the main BigQuery table to be updated.
        staging_table_id: The ID of the staging table where new or updated
                          data is temporarily stored (streamed into).
    """
    client = bigquery.Client(project=project_id)

    main_table_full_path = f"`{project_id}.{dataset_id}.{main_table_id}`"
    staging_table_full_path = f"`{project_id}.{dataset_id}.{staging_table_id}`"

    # IMPORTANT: You need to customize this MERGE statement.
    # - Ensure 'case_id' is the primary key or suitable join key for your tables.
    # - Adjust the SET and INSERT clauses to match your table's schema.
    # - If you need to DELETE records from the main table that are no longer
    #   present in the staging table, add a 'WHEN NOT MATCHED BY SOURCE THEN DELETE' clause.
    #   However, ensure your staging table accurately represents records to be kept.
    merge_query = f"""
    MERGE {main_table_full_path} T
    USING {staging_table_full_path} S
    ON T.case_id = S.case_id
    WHEN MATCHED THEN
      UPDATE SET
        T.decision = S.decision,
        T.decision_at = S.decision_at,
        T.decision_by = S.decision_by,
        T.status = S.status,
        T.updated_at = S.updated_at
    WHEN NOT MATCHED THEN
      INSERT (case_id, decision, decision_at, decision_by, status, updated_at)
      VALUES (S.case_id, S.decision, S.decision_at, S.decision_by, S.status, S.updated_at);
    """

    print(f"Executing MERGE query to address streaming buffer issue for {main_table_id}...")
    try:
        query_job = client.query(merge_query)
        query_job.result()  # Waits for the job to complete.
        print(f"MERGE operation completed successfully. Affected rows: {query_job.num_dml_affected_rows}")
        print(f"Remember to clear or truncate the staging table ({staging_table_id}) after a successful merge operation.")
    except Exception as e:
        print(f"Error during MERGE operation: {e}")
        raise

# To use this fix:
# 1. Ensure you have the 'google-cloud-bigquery' library installed (`pip install google-cloud-bigquery`).
# 2. Authenticate your GCP environment (e.g., `gcloud auth application-default login`).
# 3. Replace the placeholder values with your actual project, dataset, and table IDs.
# 4. **CRITICALLY: Adapt the MERGE statement to your specific schema and update/delete logic.**
# 5. Call the function:
# fix_streaming_update_issue(
#     project_id="ai-practice-388514",
#     dataset_id="case_management",
#     main_table_id="cases",
#     staging_table_id="cases_staging" # Make sure this staging table exists and has the necessary data
# )
