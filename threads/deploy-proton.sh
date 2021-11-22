export AWS_DEFAULT_REGION=us-east-1
account_id=`aws sts get-caller-identity --query Account --output text`

aws proton create-service \
  --name "api-threads" \
  --repository-connection-arn arn:aws:codestar-connections:us-east-1:${account_id}:connection/1b441b6a-0161-4510-8f06-ca4130fd6e16 \
  --repository-id "dchristian3188/workshop-movingupstack-api-threads" \
  --branch "master" \
  --template-name Fargate-Public-Loadbalanced-Service-Redis-MySQL \
  --template-major-version 6 \
  --spec file://api-threads.yaml