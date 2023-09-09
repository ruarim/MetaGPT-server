# /usr/local/bin/ python
# get documents output by metagpt and upload to s3
# also create references to the files in the database
import os
from typing import TypedDict
import boto3
from services.db import Db

Document = TypedDict('Document', {'name': str, 'path': str, })


class FileUploader:
    # aws config
    aws_region = 'eu-west-2'

    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_project_to_s3(self, user_id, project_id, project_path: str, files: [str], folders: [str], prefix: str = ''):
        for file in files:
            path = os.path.join(
                project_path, file)
            s3_path = self.upload_file(path, file, prefix)
            # create document model and save

        for folder in folders:
            path = os.path.join(project_path, folder)
            s3_path = self.upload_folder(path, folder, prefix)
            # create document model and save
            # document = Document(
            #     user_id, url['name'], url['url'], url['type'], db
            # )
            # document.save()

    def upload_folder(self, path, folder, _prefix):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                prefix = os.path.join(_prefix, folder)
                return self.upload_file(file_path, file, prefix)

    def upload_file(self, local_path, file_name, prefix):
        s3_path = os.path.join(prefix, file_name)

        self.s3.upload_file(local_path, self.bucket_name, s3_path)
        return s3_path
