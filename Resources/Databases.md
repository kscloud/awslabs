# Databases on AWS

## RDS
Relational Database Service provides databases for OLTP (Online Transaction Processing)

## Types of databases
* Aurora - MySQL Compatible
* MySQL
* PostgreSQL
* Oracle
* Microsoft SQL
* MariaDB

RDS allows creating Read Replicas for Databases.  

* RDS handles failovers automatically
* Backup through snapshots
* Supports highly available multi-az deployments

## DynamoDB - NoSQL Database

Managed NoSQL database service.

* Push button scaling, supports scaling on the fly without downtime
* Stored on SSD storage
* Spread across 3 geographically distinct data centres
* Eventual Consistent Reads (default)
* Strongly Consistent Reads possible to enable (for additional cost)


## Redshift - OLAP (Online Analytical Processing)

Managed cloud data warehouse allowing for analysis of large data sets using standard SQL over standard ODBC/JDBC connections. Redshift is a columnar store.

* Redshift uses block size of 1MB for columnar storage
* Single Node configuration (up to 160gb of storage)
* Multi-Node - Leader Node (manages client connections and receives queries), Compute Node (store data and performs queries and computations). Up to 128 Compute Nodes


## AWS Timestream

Timeseries database - new, early release.