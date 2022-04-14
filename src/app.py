import json

import boto3

from utils import get_distro_data, upload_to_s3

DEFAULT_AWS_REGION = "us-east-1"
S3_BUCKET_NAME = 'test-bucket-ec2-0229812894'

es2_resource = boto3.resource('ec2', region_name=DEFAULT_AWS_REGION)
instances = es2_resource.instances.all()

instances_info_dict = {}

for instance in instances:
    distro_data = get_distro_data(instance.public_ip_address, "lsb_release -a") or {}
    instances_info_dict[instance.id] = dict(
        id=instance.id,
        state=instance.state["Name"],
        public_ip_address=instance.public_ip_address,
        public_dns_name=instance.public_dns_name,
        platform=f'{instance.platform_details} {instance.architecture}',
        distro_data=distro_data,
        tags=instance.tags
    )


upload_to_s3(
    bucket_name=S3_BUCKET_NAME,
    group_name='ec2-test',
    data=json.dumps(instances_info_dict)
)
