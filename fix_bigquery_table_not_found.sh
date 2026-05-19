#!/bin/bash

# Fix for "Not found: Table <project>:<dataset>.<table>" error in BigQuery.
# This script creates a dummy table. You should replace the schema with your actual table schema.

PROJECT_ID="ai-practice-388514"
DATASET_ID="loan_applications"
TABLE_ID="historical_ratios"
LOCATION="US" # Ensure this matches the location in the error message

# Define your table schema in JSON format.
# Example:
# SCHEMA='[{"name":"DSCR","type":"FLOAT"},{"name":"ICR","type":"FLOAT"},{"name":"Debt_Equity","type":"FLOAT"},{"name":"Current_Ratio","type":"FLOAT"},{"name":"EBITDA_Margin","type":"FLOAT"},{"name":"industry_code","type":"STRING"},{"name":"period_end","type":"DATE"}]'
#
# IMPORTANT: Replace this with the actual schema of your historical_ratios table.
SCHEMA='[{"name":"column1","type":"STRING"},{"name":"column2","type":"INTEGER"}]' # Placeholder schema

echo "Attempting to create table ${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}..."

bq mk \
    --table \
    --schema "${SCHEMA}" \
    --description "Automatically created table to fix 'Not found' error" \
    --time_partitioning_field period_end \
    --time_partitioning_type DAY \
    --time_partitioning_expiration 604800 \
    --clustering_fields industry_code \
    --require_partition_filter \
    "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}"

if [ $? -eq 0 ]; then
    echo "Table ${TABLE_ID} created successfully in dataset ${DATASET_ID}."
else
    echo "Failed to create table ${TABLE_ID}. It might already exist or there's another issue."
fi

echo "Consider reviewing your queries to ensure correct table names and locations."
