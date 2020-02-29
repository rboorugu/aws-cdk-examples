from aws_cdk import (
    aws_s3 as s3,
    core
)

class NewS3Bucket(core.Stack):

     def __init__(self, scope: core.Construct, id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, 
                    "MyFirstBucket", 
                    versioned=True,)