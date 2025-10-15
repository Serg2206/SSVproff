#!/usr/bin/env bash
set -euo pipefail
dvc remote add -d b2 s3://ssvproff-data || true
dvc remote modify b2 endpointurl https://s3.us-west-000.backblazeb2.com
dvc remote modify b2 access_key_id "$B2_KEY_ID"
dvc remote modify b2 secret_access_key "$B2_APP_KEY"
echo "DVC remote configured (example)."
