# Virtual Private Cloud

Main components of VPCs are

* Internet Gateways IGW
* Route Tables
* Network Access Control Lists
* Subnets
* Security Groups
* NAT Gateways

## VPC Characteristics
* It is possible to connect VPC with on-premise using VPN Gateway
* By default VPC has no inbound/outbound internet traffic (because it has no Internet Gateway attached)
* AWS VPC has a transparent VPC Router that allows cross-subnet traffic, it is invisible to the AWS users
* To monitor VPC traffic it is required to enable VPC Flow Logs which are captured to AWS CloudWatch
* It is possible to connect multiple VPCs with each other using VPC peering or Transit Gateway. 
* An Internet gateway is horizontally-scaled, redundant, and highly available. It imposes no bandwidth constraints.

## Subnets
* Subnets cannot span multiple Availability Zones
* By default all resources can communicate across subnets within a VPC. Isolating subnets from each other must be made using Network Access Control Lists.
* Subnets can be associated to one or more route tables which can be define by the AWS user
* Public Subnet in AWS is subnet that have route to the Internet Gateway
* Private Subnet is a subnet that have no route to Internet Gateway
* AWS reserves both the first four and the last IP address in each subnet CIDR block

## Example diagram

![VPC Diagram](/data/images/vpc-diagram.png)

## Security Groups and ENIs
Security Groups are stateful and can only allow traffic. Initially `Security Group` denies all traffic, they do not have deny rules, only allow rules.

## Elastic Network Interfaces
An elastic network interface is a logical networking component in a VPC that represents a virtual network card. It can include attributes like

* Primary private IPv4 address
* One or more secondary IPv4 addresses from VPC range
* One Elastic IP Address
* A MAC address
* A source/destination check