#!/usr/bin/env python3

from aws_cdk import core

from ecs.ecs_fargate_service import FargateService
from s3.new_s3_bucket import NewS3Bucket

#this region and account are needed to be injected for some of the constructs like pulling an existing vpc
region = 'us-east-1'
account='[fill in account id]'

app = core.App()
env_cn = core.Environment(region=region,account=account)
FargateService(app, "FargateService", env=env_cn)
NewS3Bucket(app, "NewS3Bucket", env=env_cn)

app.synth()
