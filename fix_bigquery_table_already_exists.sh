#!/bin/bash

# Fix for "Already Exists: Table <project>:<dataset>.<table>" error in BigQuery.
# This script creates or replaces a table using 'CREATE OR REPLACE TABLE'.
# Replace the schema with your actual table schema.

PROJECT_ID="ai-practice-388514"
DATASET_ID="sap_data"
TABLE_ID="purchase_orders"

# Define your table schema in SQL DDL format.
# IMPORTANT: Replace this with the actual schema of your purchase_orders table.
# Example:
# SCHEMA_DDL="""
#   PurchaseOrder STRING NOT NULL,
#   PurchaseOrderType STRING,
#   PurchaseOrderDate STRING,
#   ...
# """
SCHEMA_DDL="""
  column1 STRING,
  column2 INTEGER
"""

echo "Attempting to create or replace table ${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}..."

bq query --use_legacy_sql=false \
"CREATE OR REPLACE TABLE \`${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\` ( \n  ${SCHEMA_DDL} \n);"

if [ $? -eq 0 ]; then
    echo "Table ${TABLE_ID} created or replaced successfully in dataset ${DATASET_ID}."
else
    echo "Failed to create or replace table ${TABLE_ID}. Please check the error message above."
fi

echo "Consider reviewing your data pipeline or table creation logic to ensure tables are not inadvertently recreated."
