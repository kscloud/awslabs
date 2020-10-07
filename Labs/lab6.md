# Adding a s3 bucket 

In this lab we are gonna:

* Create a new S3 bucket for storing Posts
* Create a new lambda function that will be storing Posts metadata in the flask database
* A S3 event trigger that will call the lambda function each time new file is uploaded to the S3 bucket

Let's start by quickly adding a new bucket to `s3.tf`

```terraform
resource "aws_s3_bucket" "posts" {
  bucket = "posts-bucket-${random_string.bucket_random_postfix.result}"
  acl    = "private"

  tags = {
    Name = "posts-bucket-${random_string.bucket_random_postfix.result}"
  }
}

output "s3_posts_bucket" {
    value = aws_s3_bucket.posts.bucket
}
```

We need to create an IAM role for our lambda function that will provide it with VPC execution permission and to write logs to `AWS CloudWatch` service. 

Append to `iam.tf`

```terraform
resource "aws_iam_role" "lambda_mysql_loader" {
  name = "lambda_mysql_loader"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_mysql_loader_vpc_exec_role" {
  role       = aws_iam_role.lambda_mysql_loader.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
```

Now let's create a new lambda function. The function deployment package has been created beforehand and is stored under `lambda` directory. Because the lambda function will be deployed within a `VPC` it must have a Security Group. 

```terraform
resource "aws_security_group" "lambda_mysql_loader" {
  name        = "lambda_mysql_loader"
  description = "Allow egress traffic from lambda"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lambda_function" "lambda_mysql_loader" {
  filename      = "../lambda/lambda_mysql_loader.zip"
  function_name = "lambda_mysql_loader"
  role          = aws_iam_role.lambda_mysql_loader.arn
  handler       = "lambda_mysql_loader.handler"
  timeout       = 60

  source_code_hash = filebase64sha256("../data/lambda/lambda_mysql_loader.zip")

  runtime = "python3.7"

  environment {
      variables = {
        DB_USERNAME = var.flask_db_username
        DB_PASSWORD = var.flask_db_password
        DB_NAME = var.flask_db_name
        DB_ADDRESS = aws_db_instance.flask.address
      }
  }

  vpc_config {
      subnet_ids = [aws_subnet.public_subnet1.id, aws_subnet.public_subnet2.id]
      security_group_ids = [aws_security_group.lambda_mysql_loader.id]
  }
}
```

Few important things to note

* Our function has timeout of 60 seconds - in case function attempts to work longer it will be terminated
* We are passing database connection details using environment variables
* We use the python3.7 runtime

We want our lambda function to be called each time when new object is created on S3 bucket. We will achive that through S3 bucket event trigger. To configure it we need to provide S3 bucket with a permission to call the lambda function and configure the notification.

Append to the bottom of the `s3.tf`

```terraform
resource "aws_lambda_permission" "posts_bucket" {
  statement_id  = "AllowMysqlLoaderExecutionPostsFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_mysql_loader.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.posts.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.posts.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_mysql_loader.arn
    events              = ["s3:ObjectCreated:*"]
  }
}
```

* We create the event only on s3:ObjectCreated action. It will not run if the object is modified or deleted.

Last things are missing.

* Our lambda function needs to be able to reach the database - the database security group should allow lambda security group on port 3306
* Our EC2 instance should be able to connect to the database too - we need to provide it with connection details

First let's whitelist lambda on database SG:

```diff
diff --git a/rds.tf b/rds.tf
index fe73fd6..d8b9335 100644
--- a/rds.tf
+++ b/rds.tf
@@ -16,7 +16,7 @@ resource "aws_security_group" "flask_db_security_group" {
     from_port   = 3306
     to_port     = 3306
     protocol    = "tcp"
-    security_groups = [aws_security_group.flask_security_group.id]
+    security_groups = [aws_security_group.flask_security_group.id, aws_security_group.lambda_mysql_loader.id]
   }
 }
 ```

 And now let's provide the flask EC2 with the database connection details

```diff
diff --git a/ec2.tf b/ec2.tf
index d278066..fa79e4b 100644
--- a/ec2.tf
+++ b/ec2.tf
@@ -57,6 +57,11 @@ resource "aws_instance" "flask" {
 #!/bin/bash
 apt-get update
 apt-get install -y docker.io
+
+echo DB_USERNAME=${var.flask_db_username} >> /root/envfile
+echo DB_PASSWORD=${var.flask_db_password} >> /root/envfile
+echo DB_NAME=${var.flask_db_name} >> /root/envfile
+echo DB_ADDRESS=${aws_db_instance.flask.address} >> /root/envfile
 echo CATS_BUCKET=${aws_s3_bucket.cats.bucket} >> /root/envfile
 
 docker run --env-file /root/envfile --rm -it -d -p80:5000 kszarlej/flaskapp pipenv run flask run -h 0.0.0.0 -p 5000
 ```

 Let's apply the changes

 ```bash
 terraform apply
 ```

 The apply might take a significant amount of time since it has to create and modify many resources. 

 Congratulations, you have deployed your first event based system on AWS. In the next lab we will test it.