
from google.cloud import bigquery

def perform_batch_update_on_streaming_table(project_id, dataset_id, table_id, update_sql_logic, temp_table_suffix="_temp"):
    """
    Performs an "update" operation on a BigQuery table that might be receiving streaming inserts.
    This approach creates a new table with the updated data and then replaces the original table.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): Your BigQuery dataset ID.
        table_id (str): Your BigQuery table ID (e.g., "case_management.cases").
        update_sql_logic (str): The SQL logic for your UPDATE/DELETE operation.
                                This should be a SELECT statement that returns the *final* desired state of the table.
                                For example: "SELECT * EXCEPT(decision, decision_at, decision_by, status, updated_at),
                                              @dec AS decision, TIMESTAMP(@ts) AS decision_at, @actor AS decision_by,
                                              @dec AS status, TIMESTAMP(@ts) AS updated_at
                                              FROM `ai-practice-388514.case_management.cases` WHERE case_id != @cid
                                              UNION ALL
                                              SELECT * EXCEPT(decision, decision_at, decision_by, status, updated_at),
                                              @dec AS decision, TIMESTAMP(@ts) AS decision_at, @actor AS decision_by,
                                              @dec AS status, TIMESTAMP(@ts) AS updated_at
                                              FROM `ai-practice-388514.case_management.cases` WHERE case_id = @cid"
                                              (This is a simplified example, actual logic needs careful construction.)
        temp_table_suffix (str): Suffix for the temporary table.
    """
    client = bigquery.Client(project=project_id)
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    temp_full_table_id = f"{project_id}.{dataset_id}.{table_id}{temp_table_suffix}"

    print(f"Starting batch update for table: {full_table_id}")

    # 1. Create a new table with the updated data
    # This example assumes update_sql_logic is a SELECT statement that produces the desired final table state.
    # For a DELETE, it would be a SELECT * WHERE NOT <condition>
    # For an UPDATE, it would be a SELECT with modified columns for target rows, and original columns for others.
    create_temp_table_query = f"""
    CREATE OR REPLACE TABLE `{temp_full_table_id}` AS
    {update_sql_logic}
    """
    print(f"Creating temporary table with query:
{create_temp_table_query}")
    query_job = client.query(create_temp_table_query)
    query_job.result()  # Waits for the query to finish
    print(f"Temporary table `{temp_full_table_id}` created/updated.")

    # 2. Replace the original table with the temporary table
    # This is an atomic operation.
    replace_table_query = f"""
    ALTER TABLE `{full_table_id}` REPLACE DEDICATED PARTITION FOR SYSTEM_TIME_AS OF CURRENT_TIMESTAMP()
    WITH TABLE `{temp_full_table_id}`;
    """
    # Note: The above ALTER TABLE REPLACE DEDICATED PARTITION is for partitioned tables.
    # For a non-partitioned table, you might need to drop the old and rename the new,
    # or use CREATE OR REPLACE TABLE.
    # A simpler, more general approach is:
    replace_table_query = f"""
    CREATE OR REPLACE TABLE `{full_table_id}` AS
    SELECT * FROM `{temp_full_table_id}`;
    """

    print(f"Replacing original table with temporary table using query:
{replace_table_query}")
    query_job = client.query(replace_table_query)
    query_job.result() # Waits for the query to finish
    print(f"Original table `{full_table_id}` updated successfully.")

    # 3. Optionally, drop the temporary table (or keep it for audit/rollback)
    drop_temp_table_query = f"DROP TABLE IF EXISTS `{temp_full_table_id}`;"
    print(f"Dropping temporary table `{temp_full_table_id}`.")
    query_job = client.query(drop_temp_table_query)
    query_job.result()
    print("Temporary table dropped.")

# Example Usage:
PROJECT_ID = "ai-practice-388514"
DATASET_ID = "case_management"
TABLE_ID = "cases"

# IMPORTANT: You need to construct the `update_sql_logic` carefully.
# This SQL should represent the *entire desired state* of the table *after* your update/delete.
# Example for an UPDATE (modifying a specific case_id):
# This example needs to be adapted to the specific fields and update criteria.
# It assumes you want to update specific rows and keep others as they are.
# You might need to pass parameters like @dec, @ts, @actor, @cid as job configurations.
UPDATE_SQL_LOGIC = f"""
SELECT
    t.* EXCEPT(decision, decision_at, decision_by, status, updated_at)
    REPLACE(
        'new_decision' AS decision,
        CURRENT_TIMESTAMP() AS decision_at,
        'new_actor' AS decision_by,
        'new_status' AS status,
        CURRENT_TIMESTAMP() AS updated_at
    )
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` AS t
WHERE t.case_id = 'your_target_case_id_here'
UNION ALL
SELECT *
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
WHERE case_id != 'your_target_case_id_here'
"""

# Example for a DELETE (deleting a specific case_id):
# DELETE_SQL_LOGIC = f"""
# SELECT *
# FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
# WHERE case_id != 'your_target_case_id_to_delete'
# """

# To run the fix, uncomment and adapt the following line:
# perform_batch_update_on_streaming_table(PROJECT_ID, DATASET_ID, TABLE_ID, UPDATE_SQL_LOGIC)
