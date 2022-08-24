import boto3, uuid

from django.conf import settings


client = boto3.client('s3')
config = settings.AWS_STORAGE_BUCKET_NAME
image_extension_list = ['PNG', 'png','jpg', 'JPG', 'GIF', 'gif', 'JPEG', 'jpeg']

class FileUploader:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def upload(self, file):
        try: 
            extra_args = {'ContentType' : file.content_type}
            file_id    = str(uuid.uuid4())
            
            self.client.upload_fileobj(
                file,
                config,
                file_id,
                ExtraArgs = extra_args
            )
            a = f'https://{config}.s3.{settings.AWS_REGION}.amazonaws.com/{file_id}'
            return a
        except:
            return None

    def delete(self, file_name):
        return self.client.delete_object(Bucket=config, Key=f'{file_name}')


class FileHandler:
    def __init__(self, file_uploader):
        self.file_uploader = file_uploader
    
    def upload(self, file):
        
        return self.file_uploader.upload(file)
        
    def delete(self, file_name):
        return self.file_uploader.delete(file_name)




