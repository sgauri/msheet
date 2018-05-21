#!/bin/bash

echo "Backup Started."
echo "variables initializing."
export AWS_ACCESS_KEY_ID=AKIAIIGLO5AUX5YIKLLA
export AWS_SECRET_ACCESS_KEY=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
BUCKET=maths-ws

DB_USER=root
DB_PASS=root1234
DB_HOST=127.0.0.1
DIR="/home/ubuntu/mathsheet/envm/bin/"

echo "variables initialized successfully."

echo "env activating"
cd $DIR
source activate
echo "env activated successfully."

cd ../../maths-ws/trunk

PGPASSWORD=$DB_PASS pg_dump -Fc --no-acl -h $DB_HOST -U $DB_USER math_sheet > pg_backup.json

echo "aws cmnd prepare"
/home/ubuntu/mathsheet/envm/bin/aws s3 cp pg_backup.json s3://maths-ws/backups/db/$(date "+%Y-%m-%d-%H-%M-%S")-backup.gz --sse AES256

echo "aws aws cmnd executed successfully."
rm -f pg_backup.json

echo "backup file saved successfully."

