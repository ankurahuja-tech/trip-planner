from storages.backends.s3boto3 import S3Boto3Storage

from config.settings.base import PUBLIC_MEDIA_LOCATION, STATIC_LOCATION


class StaticStorage(S3Boto3Storage):
    location = STATIC_LOCATION
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    location = PUBLIC_MEDIA_LOCATION
    default_acl = "public-read"
    file_overwrite = False
