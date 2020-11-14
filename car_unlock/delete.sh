#!/bin/bash
docker rm -f carunlock_api_1 carunlock_sql_db_1
docker image rm carunlock_api #golang:alpine mysql
