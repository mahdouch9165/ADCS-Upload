import datetime
import os
import boto3
import smart_open
from stat import S_IFREG
from stream_zip import stream_zip, ZIP_32

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
    # s3.download_file('azcopy-folder', 'azcopy', '/tmp/azcopy')
    # os.chmod('/tmp/azcopy', 0o755)
    
    # AWS Bucket for cohort data
    aws_full_path = os.environ['AWS_LINK']
    data_bucket_name = os.environ['DATA_BUCKET']
    zip_file_bucket = os.environ['ZIP_FILE_S3_BUCKET']

    smart_open_transport_params = {
        'client': s3,
    }
    
    # TODO
    # 1. Code to fetch target s3 folder
    bucket = boto3.resource('s3').Bucket(data_bucket_name)

    
    # 2. Zip up folder and store in temporary S3 of our AWS account
    
    # Azure Blob Storage
    dest_full_path = os.environ['ADDI_TOKEN']

    zip_file_s3_path = os.environ['ZIP_FILE_S3_PATH']
    zipped_chunks = stream_zip(zip_member_files(bucket, data_bucket_name, "cats/", smart_open_transport_params))
    with smart_open.open(zip_file_s3_path, 'wb') as fout:
        for zipped_chunk in zipped_chunks:
            fout.write(zipped_chunk)

    azcopy_command = f'/tmp/azcopy cp "{zip_file_s3_path}" "{dest_full_path}" --recursive=true --log-level=DEBUG'

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
    # s3.delete_object(
    #     Bucket=os.environ['ZIP_FILE_S3_BUCKET'],
    #     Key=os.environ['ZIP_FILE_S3_KEY'],
    # )

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

def zip_member_files(bucket, data_bucket_name, prefix, smart_open_transport_params):
    """
    Args:
    ---------
        bucket: A boto3 Bucket resource
        data_bucket_name: A string of the name of the s3 bucket to take data from
        prefix: A string of the prefix of files to include in the zip file
        smart_open_transport_params: Passed to smart_open.open
    """
    modification_time = datetime.datetime.now()
    mode = S_IFREG | 0o600
    
    for obj in bucket.objects.filter(Delimiter='/', Prefix=prefix):
        # Skip folders
        if obj.key[-1] == '/':
            continue
        
        print(obj)

        with smart_open.open('s3://' + data_bucket_name + '/' + obj.key, 'rb', transport_params=smart_open_transport_params) as fin:
            def file_data_generator():
                # 32 MiB chunks
                while file_data := fin.read(32 * 2**20):
                    yield file_data

            yield (obj.key, modification_time, mode, ZIP_32, file_data_generator())