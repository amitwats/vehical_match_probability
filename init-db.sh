#!/bin/bash

# Create schema in the database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS autograb_schema;
EOSQL

# Run the SQL script to create tables within the schema
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/data.sql
