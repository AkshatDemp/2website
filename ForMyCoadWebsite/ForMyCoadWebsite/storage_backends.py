from storages.backends.s3boto3 import S3Boto3Storage

class S3BlogImgStorage(S3Boto3Storage):
    location = 'blogImg'
    default_acl = 'public-read'
