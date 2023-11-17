import os
import shutil
import subprocess
import sys
import uuid
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3 as s3,
    aws_lambda as lambda_,
)
from constructs import Construct

class ACDSUploadStack(Stack):
    def _install_dependencies(self, build_folder: str):
        """Installs files from `resources/requirements.txt` into given `build_folder`
        Copies `resources/lambda_function.py` to be in same folder as dependencies
        Does not clean the build folder, so if dependecies removed, the build folder must
        manually be deleted"""
        print(os.getcwd())

        try:
            os.mkdir(build_folder)
        except FileExistsError:
            pass

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join("resources", "requirements.txt"), "-t", build_folder])
        shutil.copy(os.path.join("resources", "lambda_function.py"), build_folder)


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "zip-test-bu")

        build_folder = "build-acds-upload"
        self._install_dependencies(build_folder=build_folder)


        handler = lambda_.Function(self, "zip-test",
                                   runtime=lambda_.Runtime.PYTHON_3_11,
                                   architecture=lambda_.Architecture.ARM_64,
                                   code=lambda_.Code.from_asset(build_folder),
                                   handler="lambda_function.lambda_handler",
                                   timeout=Duration.seconds(30),
                                   environment=dict(
                                        AWS_LINK="TODO",
                                        ADDI_TOKEN="TODO",
                                        # Temporarily use same bucket for input data
                                        DATA_PREFIX="cats/",
                                        DATA_BUCKET=bucket.bucket_name,
                                        ZIP_FILE_S3_BUCKET=bucket.bucket_name,
                                        ZIP_FILE_S3_KEY="out.zip",
                                        ZIP_FILE_S3_PATH=f"s3://{bucket.bucket_name}/out.zip",
                                   ))
        
        bucket.grant_read_write(handler)

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
