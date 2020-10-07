# Lab 3 - Creating our first EC2

In this lab we are gonna create an EC2 instance with a sample app. The application will be reading and display photos from an S3 Bucket.

Let's start with defining the keypair used to access the instance.

Create a new `ec2.tf` file

```terraform
resource "aws_key_pair" "key_pair" {
  key_name   = "flask_key_pair"
  public_key = var.ssh_pubkey
}
```

This will create an AWS keypair. This key will be injected into EC2 instance authorized_keys.

Every EC2 instance has to be created from an `Amazon Machine Image` (AMI). Images can be `private` (you can create your own) or `public`. Using terraform we can easily query a newest Ubuntu image published by [Canonical Ltd](https://canonical.com/) as public image.

Add to `ec2.tf`

```terraform
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # canonical owner id
}
```

In order to connect to the EC2 instance using SSH we need to create a `Security Group` with port `22` opened to the traffic. This security group will be associated to the instance created in the next step. We will open port 22 for SSH and 80 for example application that our instance will host.

```terraform
resource "aws_security_group" "flask_security_group" {
  name        = "flask_security_group"
  description = "Allow traffic to flask"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

Now let's define the very basic EC2 instance. The instance will be called `flask` because soon it will host a small flask application. Additionally, we are adding an `output` on the very end to get the created EC2 instance IP address.

```terraform
resource "aws_instance" "flask" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.key_pair.key_name
  subnet_id              = aws_subnet.public_subnet1.id
  vpc_security_group_ids = [aws_security_group.flask_security_group.id]

  tags = {
      Name = "flask"
  }
}

output "flask_instance_ip_address" {
  value = aws_instance.flask.public_ip
}
```

You should be able to SSH into the instance.