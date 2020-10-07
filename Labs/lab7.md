# Test the event triggers

Let's test the event triggers by uploading few files and inspect the application. We will use a fake online REST API at https://jsonplaceholder.typicode.com/. Run the `terraform output` command and grab the `s3_posts_bucket` output which contains the posts bucket name.

Run

* curl https://jsonplaceholder.typicode.com/posts/1 | aws --profile training --region eu-west-1 s3 cp - s3://[[bucket-name]]/post1
* curl https://jsonplaceholder.typicode.com/posts/2 | aws --profile training --region eu-west-1 s3 cp - s3://[[bucket-name]]/post2

From the outputs above grab the `flask_instance_ip_address` output and open the IP address in browser. Click in the "Show posts" link and you should see table with posts. 