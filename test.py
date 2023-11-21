# import lambda_function
import os

import boto3
from botocore import UNSIGNED
from botocore.config import Config

from botocore.handlers import disable_signing

from cdk.resources import lambda_function

os.environ["AWS_LINK"] = "TODO"
os.environ["ADDI_TOKEN"] = "TODO"
os.environ["DATA_BUCKET"] = "test-zip-bu"
os.environ["DATA_PREFIX"] = "cats/"
os.environ["ZIP_FILE_S3_BUCKET"] = "test-zip-bu"
os.environ["ZIP_FILE_S3_KEY"] = "zip-out"
os.environ["ZIP_FILE_S3_PATH"] = "s3://test-zip-bu/zip-out.zip"


# s3 = boto3.resource('s3')

# s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

# bucket = s3.Bucket("sudachi")

# for obj in bucket.objects.filter(Delimiter='/', Prefix="chive/"):
#     print(obj)
#     print(obj.size)


lambda_function.lambda_handler(None, None)
