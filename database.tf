variable "database_password" {
  description = "Password for the database user"
  type        = string
}

variable "security_group" {
  description = "Security group (e.g. sg-0123456789abcdef)"
  type        = string
}

variable "subnet_group" {
  description = "Subnet group (e.g. my-subnet-group)"
  type        = string
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "14.6"
  instance_class       = "db.t3.micro"
  db_name              = "harnessff"
  username             = "postgres"
  password             = "${var.database_password}"
  publicly_accessible = true
  vpc_security_group_ids = [var.security_group]
  db_subnet_group_name      = var.subnet_group
}

output "database_endpoint" {
  value = aws_db_instance.postgres.endpoint
}