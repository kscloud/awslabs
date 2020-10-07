# IAM (Identity and Access Management)

AWS Identity and Access Management (IAM) is a web service for controlling access to AWS services. With IAM, you can centrally manage users, security credentials such as access keys, and permissions that control which AWS resources users and applications can access. 

There are three most important primitives in IAM

* Users - entity that you create in AWS to represent person or application that uses it to interact with AWS
* Groups - groups are collection of IAM Users
* Roles - similar to users but not uniquely associated with a given person or application - it can be **assumed** by any person or application that needs it (and has permission to assume it). It does not provide a long-term credentials - instead, when assuming a role, a temporary short-term **session** credentials are provided
* Policy Documents or Policies - JSON documents that specify the permissions which are then embedded into a role, user, group or a resource

## Root vs IAM User

* Root User - a very special user which can do basically everything from the start. It is created as the first user in AWS account and it is not possible to restrict root user permissions.
* IAM User - a user created in the IAM. His permissions can be restricted. 

A best practice is to use **root** user only for account initialization process, after it is done create an IAM user with `Admininistrator Access` and use this IAM user for daily work. Store the **root** credentials in a secure vault - it might be needed for some recovery actions.

## Policy types

Identity-based permissons - permissions assigned to *user*, *group* or *role*. Specify what given entity can do.
Resource-based permissions - permissions attached to given resource. Only small subset of AWS resources support them, for example, S3 buckets. 

Policies are divided into:
* Managed Policies - AWS or Customer managed policy documents
* Inline Policies - Policies which are embedded into a *user*, *group* or *role*

## Federation
With IAM you can setup federated login - e.g. use your current on-premise AD as a identity store for your IAM users.