# Lab 1 - Preparing terraform workspace

Create a new directory for the terraform workspace. Create a `main.tf` file inside the folder which will be used to configure the AWS provider.

```terraform
provider "aws" {
  region  = "eu-west-1"
  profile = "[[your aws profile name]]"
}
```

Let's try to initialize the workspace:

```bash
$ terraform init
```

This command will download all the required providers (it may take several seconds) and initialize the repo. You should be presented with a output containing  ```Terraform has been successfully initialized!``` text.

Notice the `.terraform` directory created by the `init` command.

Now let's create a `variables.tf` file that'll contain all the variables used by terraform. We will start with only a handful of variables

```terraform
variable "ssh_pubkey" {
    description = "SSH Public Key which will be whitelisted for SSH access to EC2 instances"
    default = "[[your ssh public key here]]"
}

variable "vpc_cidr" {
    description = "AWS VPC IP address class"
    default = "10.0.0.0/16"
}

variable "public_subnet1_cidr" {
    description = "IP address class for first public subnet in the VPC"
    default = "10.0.0.0/24" 
}

variable "public_subnet2_cidr" {
    description = "IP address class for first second subnet in the VPC"
    default = "10.0.1.0/24" 
} 
```