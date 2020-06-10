import boto3
import csv
import yaml
import datetime

X = slice(-8, 50)

# set the aws access credentials
conf = yaml.load(open('conf/aws.config'))
config_aws_access_key_id = conf['aws']['access_key_id']
config_aws_secret_access_key = conf['aws']['secret_access_key']
config_region_name = conf['aws']['region_name']


client=boto3.client('ec2',
        aws_access_key_id=config_aws_access_key_id,
        aws_secret_access_key=config_aws_secret_access_key,
        region_name=config_region_name)

paginator = client.get_paginator('describe_instances')
response_iterator = paginator.paginate()
with open('PatchLevel.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['InstanceId', 'ImageId', 'Platform', 'Patch Date', 'Patch Level in days', 'Compliance State'])
#file.close()
for iterator in response_iterator:
    for resp in iterator['Reservations']:
        VersionTag = "Version tag not found"
        AccountId = resp['OwnerId']
        for inst in resp['Instances']:
            ImageId=inst['ImageId']
            Platform=inst['Platform']
            InstanceId=inst['InstanceId']
            ec2Instance = inst['InstanceId']
            tags = {}
            for tag in inst['Tags']:
                tags[tag['Key']] = tag['Value']
            if tag["Key"] == 'Version':
                VersionTag = tag["Value"]
                VersionTag = VersionTag[X]
                patchdate = datetime.datetime.strptime(str(VersionTag), '%Y%m%d').date()
                print(patchdate)
                datetimenow = datetime.datetime.now()
                date_time_obj = datetime.datetime.strptime(str(datetimenow), '%Y-%m-%d %H:%M:%S.%f')
                todaydate = date_time_obj.date()
                patchlevel = (date_time_obj.date() - patchdate)
                patchlevel_days = patchlevel.days
                if patchlevel_days > 30:
                    compliance_comment = 'Patch level is older than 30 days'
                    compliance_state = 'no'
                    print(compliance_comment)
                else:
                    compliance_state = 'yes'
                print(ImageId,Platform,patchdate,InstanceId)
                print(patchlevel_days)
            else:
                print("this is not tagged with tag Version")
                patchdate = ""
                patchlevel_days = ""
                compliance_state = "Version tag does not exist"
            with open('PatchLevel.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([InstanceId, ImageId, Platform, patchdate, patchlevel_days, compliance_state])
                file.close()
