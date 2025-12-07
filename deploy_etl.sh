#!/bin/bash
set -euo pipefail

# deploy_etl.sh
# Packages etl-aws lambda files into lambda.zip and optionally updates an AWS Lambda function.
# Usage:
#   ./deploy_etl.sh          # create lambda.zip in etl-aws/
#   LAMBDA_NAME=my-fn ./deploy_etl.sh   # also upload to Lambda
#
# Prereqs: aws cli configured (aws configure) or AWS_* env vars

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$ROOT_DIR/etl-aws"
ZIP_NAME="lambda_payload.zip"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "Error: $PROJECT_DIR not found. Are you in the repo root?"
  exit 2
fi

echo "Packaging Lambda in $PROJECT_DIR ..."
pushd "$PROJECT_DIR" >/dev/null

# Clean old zip
[ -f "$ZIP_NAME" ] && rm -f "$ZIP_NAME"

# Create a temporary staging folder to include necessary files only
TMP_DIR="$(mktemp -d)"
cp lambda_function.py transform.py "$TMP_DIR/" 2>/dev/null || true

# If you have local dependencies vendored, add them here (example: packages/ )
# cp -r packages/* "$TMP_DIR/" 2>/dev/null || true

pushd "$TMP_DIR" >/dev/null
zip -r "../$ZIP_NAME" .
popd >/dev/null

# move zip to project root
mv "$ZIP_NAME" "$PROJECT_DIR/$ZIP_NAME"
rm -rf "$TMP_DIR"

popd >/dev/null

echo "Created $PROJECT_DIR/$ZIP_NAME"

# Optionally upload to AWS Lambda
if [ -n "${LAMBDA_NAME:-}" ]; then
  echo "Uploading to AWS Lambda function: $LAMBDA_NAME"
  aws lambda update-function-code --function-name "$LAMBDA_NAME" --zip-file "fileb://$PROJECT_DIR/$ZIP_NAME"
  echo "Update triggered (check AWS console / CloudWatch logs for confirmation)."
else
  echo "To deploy to AWS Lambda, set LAMBDA_NAME environment variable and run:"
  echo "  LAMBDA_NAME=my-lambda ./deploy_etl.sh"
fi
