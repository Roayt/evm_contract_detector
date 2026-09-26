#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
CREATE ROLE detector WITH LOGIN PASSWORD '$DETECTOR_PASSWORD';
GRANT CONNECT ON DATABASE evm_detector TO detector;
GRANT USAGE ON SCHEMA public TO detector;
GRANT SELECT,INSERT ON contract TO detector;
GRANT USAGE ON SEQUENCE contract_id_seq TO detector;
GRANT SELECT,INSERT,UPDATE ON check_point TO detector; 
EOSQL
