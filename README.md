# Setup

## Create Cloud Database

### Warning
_AWS Costs Money_

### Environment variables 
Prior to running Terraform, create necessary environment variables

```
export DATABASE_PASSWORD="harnessisbest"
export SECURITY_GROUP="sg-abc123"
export SUBNET_GROUP="default-vpc-abc123"
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```

### Run Terraform

_Disclaimer: Everyone's environment is different, you may need to tweak the Terraform to comply with your governance and/or security rules._
```
 terraform init
 
 terraform apply -var "database_password=$DATABASE_PASSWORD"  -var "security_group=$SECURITY_GROUP" -var "subnet_group=$SUBNET_GROUP"
```
![alt text](images/terraform.png)
### Load Data
Once your DB is created by Terraform you will receive the endpoint information.

Rename `config.ini.sample` to `config.ini` and modify the values for `host`, `port`, `user`, and `password` as appropriate for your environment.

Run the Python loader script in a docker container. This can be done locally, but that approach is not recommended.

```commandline
docker run -it -v $(pwd)/config.ini:/config.ini -v $(pwd)/init_aws_db.py:/init_aws_db.py --rm python:3.8.2 pip3 install psycopg2-binary ; python3 init_aws_db.py
```
![alt text](images/loader.png)

