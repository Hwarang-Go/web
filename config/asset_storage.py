from storages.backends.s3boto3 import S3Boto3Storage

# For S3 media path
class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

