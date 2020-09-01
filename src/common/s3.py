import boto3
import logging
from botocore.exceptions import ClientError


class S3:
    def __init__(self):
        self.client = boto3.client('s3')

    # Consider moving client to libs
    def upload(self, filename, bucket, object_name=None):
        if object_name is None:
            object_name = filename

        try:
            self.client.upload_file(filename, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_obj(self, filename, bucket, object_name):
        try:
            with open(filename, "rb") as f:
                self.client.upload_fileobj(f, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
