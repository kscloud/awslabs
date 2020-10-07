# Configuring the MySQL database

In this lab we will learn how to configure MySQL settings.

## Parameter Groups

In RDS databases are configured through `Parameter Groups`. By default when a new database is created a default parameter group for given `engine` (MySQL/PostgreSQL etc) and `engine_version` (8.0, ). For example, for database created in lab 5 a `default.mysql8.0` option group has been created:

![Default Parameter Group](/data/images/pg1.png)

A default parameter group cannot be modified, if we want to modify some database settings we must create a parameter group. 

Let's create a MySQL parameter group in `rds.tf`. We want to modify the `character_set_server` and `character_set_client` directives to `utf8`.

```terraform
resource "aws_db_parameter_group" "flask_mysql80" {
  name   = "mysql80-flask-parameter-group"
  family = "mysql8.0"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }

  parameter {
    name  = "character_set_client"
    value = "utf8"
  }
}
```

Now we need to modify our database to use this parameter group.

```diff
diff --git a/rds.tf b/rds.tf
index d8b9335..f4747c2 100644
--- a/rds.tf
+++ b/rds.tf
@@ -29,7 +29,7 @@ resource "aws_db_instance" "flask" {
   name                 = var.flask_db_name
   username             = var.flask_db_username
   password             = var.flask_db_password
+  parameter_group_name = aws_db_parameter_group.flask_mysql80.name
   multi_az             = false
   vpc_security_group_ids = [aws_security_group.flask_db_security_group.id]
   db_subnet_group_name = aws_db_subnet_group.main.name
```

Apply the changes.

```bash
terraform apply
```

After apply has finished the `Parameter Group` will not be live yet. Database will enter `pending-reboot` mode as shown on below image. 

![Pending Reboot](/data/images/pg2.png)

## Multi Availability Zone

Our database is configured as `Single-AZ` meaning that only single database instance is deployed in a single `Availability Zone`, we have zero fault tolerance. 

RDS gives us a possibility to configure the database as `Multi-AZ`. A second, standby instance, will be created in a separate AZ. In case of primary instance failure it will be promoted to master.

We can easily configure our flask RDS to a `Multi-AZ` mode

```diff
diff --git a/rds.tf b/rds.tf
index fe73fd6..09c3617 100644
--- a/rds.tf
+++ b/rds.tf
@@ -30,7 +30,7 @@ resource "aws_db_instance" "flask" {
   username             = var.flask_db_username
   password             = var.flask_db_password
   parameter_group_name = "default.mysql8.0"
-  multi_az             = false
+  multi_az             = true
   vpc_security_group_ids = [aws_security_group.flask_db_security_group.id]
   db_subnet_group_name = aws_db_subnet_group.main.name
   skip_final_snapshot = true
```

You can omit this step to avoid additional costs because multi-az costs twice as much as single-az.