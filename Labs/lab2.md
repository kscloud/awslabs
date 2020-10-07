# Lab 2 - Building VPC

In this lab we are gonna create a `Virtual Private Cloud` (a VPC) that will host our application.

Let's start by creating our `vpc.tf` file
```terraform
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}

resource "aws_subnet" "public_subnet1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet1_cidr
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_subnet2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet2_cidr
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}
```

Run apply

```
terraform apply
```

The above code creates a very basic VPC with just two public subnets. Notice that each subnet has unique `availability_zone` attribute - in AWS subnets cannot span multiple availability zones. Additionally, the `map_public_ip_on_launch` parameter gives AWS permission to assign public IP addresses to resources created in these subnets - we gonne need this during EC2 instance creation - without public IP we wouldn't be able to connect to it.

By default a VPC in AWS does not have an internet access, and there is no internet access to it neither. There is a special virtual device called `Internet Gateway` that needs to be created and attached to the VPC to allow the from/to internet access.

Let's add it in `vpc.tf`

```terraform
##
#  Internet Gateway
##
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main"
  }
}
```

Now one more thing is missing, the routing configuration. We need to create a `Route Table` with proper route and associate our two public subnets with it.

```terraform
##
#  Routing configuration
##
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "main"
  }
}

resource "aws_route_table_association" "public_subnet1" {
  subnet_id      = aws_subnet.public_subnet1.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "public_subnet2" {
  subnet_id      = aws_subnet.public_subnet2.id
  route_table_id = aws_route_table.main.id
}
```

After the public subnets are associated with the `main` Route Table the entire traffic will be routed to the `Internet Gateway`. Few important things to note:

* There is no explicit route for local traffic between resources within/cross subents - the local route is implicitly added by AWS
* In AWS by default subnets can communicate with each other - there are no firewalls/ACLs between them unless you setup one yourself

Run apply

```bash
$ terraform apply
```