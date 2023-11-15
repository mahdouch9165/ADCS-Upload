import os
import subprocess
import boto3

def find_azcopy_log():
    for file_name in os.listdir('/tmp'):
        if 'log' in file_name.lower():
            return os.path.join('/tmp', file_name)
    return None
    
def upload_logs_to_s3(log_file_path):
    s3 = boto3.client('s3')
    log_file_name = os.path.basename(log_file_path)
    s3.upload_file(log_file_path, 'azcopy-folder', 'logs/' + log_file_name)

def lambda_handler(event, context):
    # AWS Credentials
    os.environ["AZCOPY_LOG_LOCATION"] = "/tmp"
    os.environ["AZCOPY_JOB_PLAN_LOCATION"] = "/tmp"
    
    # Download AzCopy executable from S3
    s3 = boto3.client('s3')
    s3.download_file('azcopy-folder', 'azcopy', '/tmp/azcopy')
    os.chmod('/tmp/azcopy', 0o755)
    
    # AWS Bucket for cohort data
    aws_full_path = os.environ["AWS_LINK"]
    
    # TODO
    # 1. Code to fetch target s3 folder
    
    # 2. Zip up folder and store in temporary S3 of our AWS account
    
    # Azure Blob Storage
    dest_full_path = os.environ["ADDI_TOKEN"]

    # azcopy_command = f'/tmp/azcopy cp "{aws_full_path}" "{dest_full_path}" --recursive=true --log-level=DEBUG'

    # try:
    #     result = subprocess.run(azcopy_command, check=True, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     print(f"AzCopy stdout:\n{result.stdout}")
    #     print(f"AzCopy stderr:\n{result.stderr}")
    # except subprocess.CalledProcessError as e:
    #     print(f"AzCopy command failed with return code {e.returncode}:")
    #     print(f"AzCopy stdout:\n{e.stdout}")
    #     print(f"AzCopy stderr:\n{e.stderr}")
        
    # TODO
    # 3. Delete local S3 zipped folder
        
    # Upload the logs to S3
    # log_file_path = find_azcopy_log()
    # if log_file_path:
    #     upload_logs_to_s3(log_file_path)
    # else:
    #     print("AzCopy log file not found")

    return {
        'statusCode': 200,
        'body': 'AzCopy process completed.'
        
}