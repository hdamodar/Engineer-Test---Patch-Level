import boto3
import csv
import yaml
import datetime

X = slice(-8, 50)

client=boto3.client('ec2', region_name='ap-southeast-2')

paginator = client.get_paginator('describe_instances')
response_iterator = paginator.paginate()
with open('PatchLevel.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Instance Id', 'AMI ID', 'Platform', 'Patch Date', 'Patch Level in days', 'compliance status'])
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
                #print(patchdate)
                datetimenow = datetime.datetime.now()
                date_time_obj = datetime.datetime.strptime(str(datetimenow), '%Y-%m-%d %H:%M:%S.%f')
                todaydate = date_time_obj.date()
                date_diff = (date_time_obj.date() - patchdate)
                patchlevel_days = date_diff.days
                if patchlevel_days > 30:
                    compliance_comment = 'Patch level is older than 30 days'
                    compliance_state = 'non-compliant'
                    #print(compliance_comment)
                else:
                    compliance_state = 'compliant'
                #print(ImageId,Platform,patchdate,InstanceId)
                #print(patchlevel_days)
            else:
                #print("this is not tagged with tag Version")
                patchdate = ""
                patchlevel_days = ""
                compliance_state = "Version tag does not exist"
            print(InstanceId, ImageId, Platform, patchdate, patchlevel_days, compliance_state)
            with open('PatchLevel.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([InstanceId, ImageId, Platform, patchdate, patchlevel_days, compliance_state])
                file.close()
