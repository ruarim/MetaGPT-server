from flask import Flask
from services.file_uploader import FileUploader
from services.metagpt import runModel
from services.db import Db
from models.document import Document
import os
import shutil

app = Flask(__name__)


@app.get('/')
def health_check():
    return 'app running'


@app.get("/prompt/<user_id>/<project_id>/<string:prompt>")
def generate(user_id, project_id, prompt):
    try:
        # runModel(prompt)  # add in production
        upload_model_output(user_id, project_id)
        # delete_model_output()

    except Exception as err:
        return {"message": 'MetaGPT failed: ' + err.__str__()}, 400
    return {"message": 'Prompt successful: ' + prompt}


def upload_model_output(user_id, project_id):
    model_output = 'workspace'
    project_folder = os.listdir(model_output)[0]
    project_path = os.path.join(model_output, project_folder)
    prefix = os.path.join(user_id, project_id)
    folders = [project_folder, 'docs', 'resources']
    files = ['requirements.txt']

    bucket = os.environ.get("S3_BUCKET_NAME")
    uploader = FileUploader(bucket)
    # db = Db("dbname=test user=postgres password=secret")  # from env
    uploader.upload_project_to_s3(user_id, project_id,
                                  project_path, files, folders, prefix)


def delete_model_output(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
