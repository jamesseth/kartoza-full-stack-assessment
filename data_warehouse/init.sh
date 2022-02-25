#!/bin/bash
mkdir -p /usr/share/postgresql/14/extension/ && touch /usr/share/postgresql/14/extension/pgrouting.control
apt-get -y update && apt-get install -y postgis postgresql-14-postgis-3 postgresql-14-pgrouting
export PGPASSWORD=${POSTGRES_PASSWORD}
while read PSQL_EXTENSION; do
  psql -U $POSTGRES_USER -d $POSTGRES_DB  -c "create extension ${PSQL_EXTENSION};"
done < psql_extensions.txt
