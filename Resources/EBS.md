## Elastic Block Storage

Service providing Block Storage for EC2.

## Volume Types

* SSD General Purpose GP2 - Up to 10 000 IOPS
* SSD Provisioned IOPS IO1 - More than 10 000 IOPS
* HDD Throughput optimized ST1 - frequently/sequential workloads like transactional stuff, data warehousing
* HDD Cold SC1 - less frequently accessed data, file servers
* HDD Magnetic - Standard - cheap, infrequently accessed storage, can be a boot volume

EC2 access to EBS instances is relized over the network. Heavy workloads might need EBS optimized EC2 instances which provides lower latency to EBS volume and thus higher throughput/IOPS.

