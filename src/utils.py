import datetime
import typing

import paramiko as prk
import boto3


def upload_to_s3(bucket_name: str, group_name: str, data: str) -> typing.Callable:
    client = boto3.client('s3')
    try:
        client.put_object(
            Body=data,
            Bucket=bucket_name,
            Key=f'ec_info/{group_name}-{datetime.datetime.now()}.json'
        )
    except Exception as e:
        print(f'Something went wrong! [{e}]')


def get_distro_data(instance_ip: str, command: str) -> typing.Optional[typing.Dict]:
    ssh_key = prk.RSAKey.from_private_key_file('creds/wk-keypair.pem')

    ssh_client = prk.SSHClient()
    ssh_client.set_missing_host_key_policy(
        prk.AutoAddPolicy()
    )
    distro_data = {}
    try:
        ssh_client.connect(
            username='ubuntu',
            pkey=ssh_key,
            hostname=instance_ip
        )

        stdin, stdout, stderr = ssh_client.exec_command(command)

        if command == 'lsb_release -a':

            decoded_output = stdout.read().decode()
            for row in decoded_output.split('\n')[:-1]:
                key, value = tuple(row.split('\t'))
                distro_data[key] = value

            return distro_data
    except Exception as e:
        print(f'Something went wrong! [{e}]')
