# DynamoDB Basics

In this lab we are gonna learn basics of DynamoDB.

## Note about Query and Scan
DynamoDB supports two basic methods for retrieving the data.

* Scan
* Query

Scan operation scans the entire table optionally filtering the results using provided filters. It is not a preferred method for querying DynamoDB since idea behind key-value stores, like DynamoDB, is to allow quick object lookups where the lookup time is constant and independent from database size. Which is not the case for Scan.

Query is the preferred method for retrieving data from database. You query given Key and database returns for you the Value. However you cannot query on arbitrary fields that's why you really need to think about your data and queries you will want to perform before you create the table.

## Scenario
We want to store weather measurements (Temperature and Humidity) from different weather Stations. We need a possibility to query measurements for individual stations. 

## Creating initial DynamoDB Table
Let's start with creating an example DynamoDB Table that will hold data from weather stations. 

Create a `dynamodb.tf` file and put inside
```terraform
resource "aws_dynamodb_table" "weather_table" {
  name           = "weather-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "StationId"

  attribute {
    name = "StationId"
    type = "S"
  }

  tags = {
    Name = "weather-table"
  }
}
```

DynamoDB is a schemaless database - we do not need to specify any fields like `Humidity` or `Temperature` in the table definition. Only the `indexed attributes` must have `name` and `type` specified through the `attribute` block. In our case only the `StationId` is the indexed attribute.


## Let's populate table with initial data

Run below commands


```bash
aws --profile training dynamodb put-item --table-name weather-table --item '{"StationId": {"S": "station1"}, "Temperature": {"N": "15"}, "Humidity": {"N": "30"}, "Timestamp": {"N": "'$(date +%s)'"}}'
aws --profile training dynamodb put-item --table-name weather-table --item '{"StationId": {"S": "station2"}, "Temperature": {"N": "18"}, "Humidity": {"N": "40"}, "Timestamp": {"N": "'$(date +%s)'"}}'
aws --profile training dynamodb put-item --table-name weather-table --item '{"StationId": {"S": "station3"}, "Temperature": {"N": "14"}, "Humidity": {"N": "34"}, "Timestamp": {"N": "'$(date +%s)'"}}'
aws --profile training dynamodb put-item --table-name weather-table --item '{"StationId": {"S": "station1"}, "Temperature": {"N": "15"}, "Humidity": {"N": "30"}, "Timestamp": {"N": "'$(date +%s)'"}}'
```

Now retrieve the data 

```sh
$ aws --profile training dynamodb scan --table-name weather-table
```

You should see three items. But wait. Didn't wee add four measurements? `station1` should have two measurements in table but has only one. That's because the hash key in the DynamoDB must uniquely identify an item. In our case second measurement with `StationId` set to `station1` overwritten the first one. 

One solution to that problem would be switching hash key to some kind of [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) field. But we will loose the possibility of querying data for given station. To get measurements for station with StationId `station1` you would need to query all UUIDs(Scan entire table) and filter the results using `StationId=station1` filter. That's not a good idea (even if you don't care about time you will waste tons of money because you will be billed for all redundant READ operations).

However, we have a timestamp field in the data. A combination of `StationId` and `Timestamp` uniquely identifies an item in our table. We can use that field and create a composite key. To do that we need to specify `Timestamp` field as a `range key` (sometimes called a `sort key`)

## Adding a range key to the table

Let's modify the table

```diff
@@ -4,12 +4,18 @@ resource "aws_dynamodb_table" "weather_table" {
   read_capacity  = 5
   write_capacity = 5
   hash_key       = "StationId"
+  range_key      = "Timestamp"

   attribute {
     name = "StationId"
     type = "S"
   }

+  attribute {
+    name = "Timestamp"
+    type = "N"
+  }
+
   tags = {
     Name = "weather-table"
   }
}
```

Now run terraform apply. Terraform will recreate the database because it is not possbile to add a `range key` to existing database. Database has to be created with a range key from the very beginning.

Now when we have the database with a range key defined lets add the data once again using set of above curls and get again retrieve the data. Now all measurements should be present in the database.

With a `composite key` we can easily query, for example, all measurements from `station1`:

```bash
aws --profile training dynamodb query --table-name weather-table --key-condition-expression "StationId = :station" --expression-attribute-values '{":station":{"S":"station1"}}'
```

Dynamodb will also automatically sort the results using range key.