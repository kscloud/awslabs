## FAQs
A very good source of information about various AWS services are FAQs published by AWS:
* EC2 https://aws.amazon.com/ec2/faqs/
* VPC https://aws.amazon.com/vpc/faqs/
* RDS https://aws.amazon.com/rds/faqs/ 
* SQS https://aws.amazon.com/sqs/faqs/
* EBS https://aws.amazon.com/ebs/faqs/

Rest of the FAQs can be found here: https://aws.amazon.com/faqs/

## Whitepapers
Amazon publishes a lot of whitepapers https://aws.amazon.com/whitepapers/. In my opinion two very good whitepapers are

* AWS Security Best Practices
* AWS Well-Architected Framework 

## Talks
* Great DynamoDB talk - https://www.youtube.com/watch?v=HaEPXoXVf2k

## Random tips

Few rules I often try to follow when building stuff on AWS 

* Using Infrastructure as Code can greatly improve the infrastructure operations and delivery speed. I use the manual web console only during testing/making MVPs. You can find a lot of reusable snippets(e.g. entire [Terraform modules](https://github.com/terraform-aws-modules)) online which will greatly speed up the infrastructure development
* Managed services are great but pretty often they are pretty expensive, sometimes it is good to think about implementing parts of the infrastructure using EC2 instances.
* Whenever you need to run code in response to an event think about AWS Lambda. AWS Lambda is super cheap
* Think about the traffic - data-heavy application might generate a lot of VPC-outbound or VPC-cross availability zone traffic. Traffic (depending on Region) costs around $0.15 per GB.

## Calculating the estimated costs of infrastructure
Use the [good oldschool AWS calculator](https://calculator.s3.amazonaws.com/index.html) or newer [Pricing Calculator](https://calculator.aws/).