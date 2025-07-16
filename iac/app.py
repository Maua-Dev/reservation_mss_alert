#!/usr/bin/env python3
import os

import aws_cdk as cdk
from adjust_layer_directory import adjust_layer_directory

from stacks.iac_stack import IacStack



print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory(shared_dir_name="shared", destination="lambda_layer_out_temp")
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")
github_ref = os.environ.get("GITHUB_REF_NAME")

stage = ''
if 'prod' in github_ref:
    stage = 'PROD'
elif 'homolog' in github_ref:
    stage = 'HOMOLOG'
elif 'dev' in github_ref:
    stage = 'DEV'
else:
    stage = 'TEST'

tags = {
    'project': 'Reservation Alerts MSS',
    'stage': stage,
    'stack': 'BACK',
    'owner': 'DevCommunity'
}

IacStack(app, stack_name, env=cdk.Environment(account=aws_account_id, region=aws_region), tags=tags)


app.synth()
