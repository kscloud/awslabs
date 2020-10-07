# Creating a MySQL Database

First lets add few new variables in `variables.tf` file with the database configuration.

```terraform
variable "flask_db_username" {
    default = "flask"
}

variable "flask_db_password" {
    default = "password"
}

variable "flask_db_name" {
    default = "flask"
}
```

To deploy an RDS database we have to create a `DB Subnet Group` which groups the subnets we designate for databases. A common practice is to create a separate VPC subnets for databases but for sake of simplicity we will just reuse the public subnets we created in lab 2.

We have to provide the database with a Security Group that will allow the flask EC2 instance to connect to it.

Now create a new `rds.tf`. 

```terraform
resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = [aws_subnet.public_subnet1.id, aws_subnet.public_subnet2.id]

  tags = {
    Name = "Main DB Subnet Group"
  }
}

resource "aws_security_group" "flask_db_security_group" {
  name        = "flask_db_security_group"
  description = "Allow traffic from flask instance to db"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.flask_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

As you can see we do not allow a certain IP block - we allow all the resources that are having the "flask_security_group" associated - so far only one EC2 instance. 

A last step is to create the database and output its endpoint.

```terraform
resource "aws_db_instance" "flask" {
  allocated_storage    = 5
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0.20"
  instance_class       = "db.t2.micro"
  name                 = var.flask_db_name
  username             = var.flask_db_username
  password             = var.flask_db_password
  parameter_group_name = "default.mysql8.0"
  multi_az             = false
  vpc_security_group_ids = [aws_security_group.flask_db_security_group.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  skip_final_snapshot = true
}

output "aws_db_instance_endpoint" {
    value = aws_db_instance.flask.endpoint
}
```

Now run `terraform apply`. Database creation might take significant amount of time (up to 10 minutes). 