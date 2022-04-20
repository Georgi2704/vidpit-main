sam validate --profile vidpit
sam build --profile vidpit --use-container --debug
sam package --profile vidpit --s3-bucket vidpit-authentication2 --output-template-file out.yml --region eu-central-1
sam deploy --profile vidpit --template-file out.yml --stack-name vidpit-authentication --region eu-central-1 --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM