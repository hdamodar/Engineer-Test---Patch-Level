#Script to list EC2 instances Patch Level

## Description

This repository contains the python script to get the list of instances with patch date and patch level compliance status and output to a csv file. Any instance patch date older than 30 days is considered non compliant.

Compliant Status:

compliant - patch level less than 30 days

non-compliant - patch level less than 30 days

blank - Tag Name 'Version' does not exist

## How the script works

- This script connects to your aws EC2 service , gets the list of EC2 instances with and checks for the tag name 'Version' for each instance.
- If tag name 'Version' exists gets the tag value "<AMI ID, config level, patch level.> e.g.
  ami-1234a567bc89d1234;20200527;20200601.
- Using Python slice() gets the Patch Level from the tag Value  and this is converted to date format.
- Checks the difference between  Patch Level date and Current date and converted to days.
- If the number of days is greater than 30 days, the instance is considered not compliant.
- The output of the script is then send to csv file that is saved to your current working directory.

## Requirement to run the python script

This script depends on boto3, the AWS SDK for Python, and requires Python.
Run the following command  to install the latest Boto3 release via pip:

pip install boto3

## Bsic Configuration:

Before running the script you should set up your AWS security credentials to connect to AWS

Replace <Your Access Key ID> and <Your Secret Access Key> with your credentials in aws.config file.

## Running Python script
This script connects to your aws EC2 service , gets the list of instnces with instance ID, Image Id, Platform, patchdate, patchlevel_days and compliance_state. All you need to do is run the code:

python patchlevel.py

## Note: ou need to make sure the credentials you're using have the correct permissions to access the Amazon EC2 service.
