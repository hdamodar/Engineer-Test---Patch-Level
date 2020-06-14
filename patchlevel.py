import boto3
import csv
import datetime
from datetime import date
import pandas as pd

instances = [i for i in boto3.resource('ec2', region_name='ap-southeast-2').instances.all()]
def get_ec2_patch_level(response):
    Instance_ID, Image_ID, Patch_Date, Patch_Level = [], [], [], []
    for i in instances:
        VersionTag = "Version tag not found"
        for t in i.tags:
            if (t["Key"] == 'Version'):
                VersionTag = t["Value"]
                patchdate = datetime.datetime.strptime(str(VersionTag)[slice(-8, 50)], '%Y%m%d').date()
                todaydate = (datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')).date()
                patch_level_diff = (todaydate - patchdate).days
                if patch_level_diff > 30:
                    Instance_ID.append(i.instance_id)
                    Image_ID.append(i.image_id)
                    Patch_Date.append(patchdate)
                    Patch_Level.append(patch_level_diff)
    return pd.DataFrame({
    'InstanceId': Instance_ID,
    'ImageID': Image_ID,
    'Patchdate': Patch_Date,
    'Patch_Level_Diff(days)': Patch_Level
    })

instances_Patch_Level_List = get_ec2_patch_level(instances)
print(instances_Patch_Level_List)