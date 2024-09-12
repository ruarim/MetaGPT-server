# /usr/local/bin/ python
# get documents output by metagpt and upload to s3
# also create references to the files in the database
import os
from typing import TypedDict
import boto3


class File(TypedDict):
    name: str
    path: str
    bucket_url: str
    bucket_name: str


class FileUploader:
    aws_region = 'eu-west-2'
    document_types = {'docs', 'resources', 'requirements'}

    def __init__(self, bucket_name: str, bucket_url: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url

    def upload_project_to_s3(self, user_id, project_id, project_path: str, requirements: str, folders: [str]):
        prefix = os.path.join(user_id, project_id)
        requirements_path = os.path.join(project_path, requirements)
        self.upload_file(requirements_path, requirements, 'requirements', prefix)

        for folder in folders:
            folder_path = os.path.join(project_path, folder)
            self.upload_folder(folder_path, folder, prefix)

    def upload_folder(self, folder_path, folder_name, _prefix):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                prefix = os.path.join(_prefix, folder_name)
                self.upload_file(file_path, file, folder_name, prefix)

    def upload_file(self, file_path, file_name, _type, prefix):
        s3_path = os.path.join(prefix, file_name)
        self.s3.upload_file(file_path, self.bucket_name, s3_path)
        type = self.get_document_type(_type)

        file: File = {
            'name': file_name,
            'path': s3_path,
            'type': type,
            'bucket_url': self.bucket_url,
            'bucket_name': self.bucket_name,
        }

        # json encode document dict -> json
        # call startupGPT api save document endpoint

    def get_document_type(self, type):
        if type not in self.document_types:
            return 'code'
        else:
            return type
