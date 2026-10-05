#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
CREATE ROLE api_reader WITH LOGIN PASSWORD '$API_READER_PASSWORD';
GRANT CONNECT ON DATABASE evm_detector TO api_reader;
GRANT USAGE ON SCHEMA public TO api_reader;
GRANT SELECT ON contract TO api_reader;
GRANT SELECT ON check_point TO api_reader; 
EOSQL
