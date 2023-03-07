# Setup

## Create Database

#### Environment variables 
Prior to running Terraform, create necessary environment variables

```
export DATABASE_PASSWORD="harnessisbest"
export SECURITY_GROUP="sg-abc123"
export SUBNET_GROUP="default-vpc-abc123"
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```

#### Run Terraform

```
 terraform init
 
 terraform apply -var "database_password=$DATABASE_PASSWORD"  -var "security_group=$SECURITY_GROUP" -var "subnet_group=$SUBNET_GROUP"
```

### Warning
AWS Costs Money