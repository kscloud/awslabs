# Lab 4 - Deploying first application
We will deploy the first application that will be getting example images from AWS object storage - `Simple Storage Service` (S3).

Let's create a S3 bucket to store images and upload few samples to it. In S3 bucket names are globally namespaced - every bucket within the entire AWS has to have an unique name. For that reason we will postfix the bucket name with a randomly generated postfix. We will also create an `output` resource so we will be able to retrieve the bucket name later on.

Create `s3.tf` file

```terraform
# Generate the random 8-character long postfix
resource "random_string" "bucket_random_postfix" {
  length = 8
  upper = false
  special = false
}

resource "aws_s3_bucket" "cats" {
  bucket = "funny-cats-bucket-${random_string.bucket_random_postfix.result}"
  acl    = "private"

  tags = {
    Name = "funny-cats-bucket-${random_string.bucket_random_postfix.result}"
  }
}

output "s3_cats_bucket" {
    value = aws_s3_bucket.cats.bucket
}
```

S3 is a webservice that provides a `RESTful API` for querying and uploading objects. We could upload the files using `curl` or other HTTP client but since we use Terraform we can also use it for that.

```terraform
resource "aws_s3_bucket_object" "funny_cat1" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat1.jpg"
  source = "../Data/funnycats/cat1.jpg"
  etag = filemd5("../Data/funnycats/cat1.jpg")
}

resource "aws_s3_bucket_object" "funny_cat2" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat2.jpg"
  source = "../Data/funnycats/cat2.jpg"
  etag = filemd5("../Data/funnycats/cat2.jpg")
}

resource "aws_s3_bucket_object" "funny_cat3" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat3.jpg"
  source = "../Data/funnycats/cat3.jpg"
  etag = filemd5("../Data/funnycats/cat3.jpg")
}

resource "aws_s3_bucket_object" "funny_cat4" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat4.jpg"
  source = "../Data/funnycats/cat4.jpg"
  etag = filemd5("../Data/funnycats/cat4.jpg")
}

resource "aws_s3_bucket_object" "funny_cat5" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat5.jpg"
  source = "../Data/funnycats/cat5.jpg"
  etag = filemd5("../Data/funnycats/cat5.jpg")
}

resource "aws_s3_bucket_object" "funny_cat6" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat6.jpg"
  source = "../Data/funnycats/cat6.jpg"
  etag = filemd5("../Data/funnycats/cat6.jpg")
}

resource "aws_s3_bucket_object" "funny_cat7" {
  bucket = aws_s3_bucket.cats.bucket
  key    = "cat7.jpg"
  source = "../Data/funnycats/cat7.jpg"
  etag = filemd5("../Data/funnycats/cat7.jpg")
}
```

In order to allow EC2 instance created in previous lab to retrieve the images from the S3 bucket we just created we need to provide it with an IAM role containing necessary permissions. 

Create `iam.tf` file

```terraform
resource "aws_iam_role" "flask" {
  name = "flask"
  path = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

data "aws_iam_policy_document" "flask" {
  statement {
    sid = "1"

    actions = [
      "s3:*"
    ]

    resources = [
      aws_s3_bucket.cats.arn,
      "${aws_s3_bucket.cats.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "flask" {
  name   = "flask"
  role   = aws_iam_role.flask.id
  policy = data.aws_iam_policy_document.flask.json
}

resource "aws_iam_instance_profile" "flask" {
  name = "flask"
  role = aws_iam_role.flask.name
}
```

First three resources define the `role`, and a `policy` that gets attached to that role. As you can see the policy contains only single statement that allows all S3 actions on the bucket and its contents. This is all we need for now. IAM roles cannot be directly attached to EC2 instances, they have to be attached through a `instance profile` - the fourth resource creates the `flask` instance profile using created role.

Now we need to modify our EC2 instance resource to make it use the created instance profile and set `user-data` script that will deploy the training application.

```diff
diff --git a/ec2.tf b/ec2.tf
index e90d5f6..d278066 100644
--- a/ec2.tf
+++ b/ec2.tf
@@ -52,6 +52,15 @@ resource "aws_instance" "flask" {
   key_name               = aws_key_pair.key_pair.key_name
   subnet_id              = aws_subnet.public_subnet1.id
   vpc_security_group_ids = [aws_security_group.flask_security_group.id]
+  iam_instance_profile   = aws_iam_instance_profile.flask.name
+  user_data = <<-EOT
+#!/bin/bash
+apt-get update
+apt-get install -y docker.io
+echo CATS_BUCKET=${aws_s3_bucket.cats.bucket} >> /root/envfile
+
+docker run --env-file /root/envfile --rm -it -d -p80:5000 kszarlej/flaskapp pipenv run flask run -h 0.0.0.0 -p 5000
+EOT
 
   tags = {
       Name = "flask"
```

Run apply 

```bash
$ terraform apply
```

When the apply has finished grab the IP address from outputs and open it in your browser. If the application does not open then EC2 may still be provisioning. Wait 1 - 2 minutes and retry. If it opened you can click on the "Get random cat" link - you should be presented with a funny cat images generator!