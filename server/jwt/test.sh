#!/usr/bin/env bash

# source env
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "$DIR/../../.env"

# delete
curl -X 'DELETE' \
  -H "Authorization: Bearer $SERVER_JWT_TOKEN"   \
  'http://192.168.1.45:3000/texts?text_id=eq.1' \
  -H 'accept: application/json'