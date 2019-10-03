from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    if settings.DJANGO_USE_S3:
        location = 'static'
    else:
        pass


class PublicMediaStorage(S3Boto3Storage):
    if settings.DJANGO_USE_S3:
        location = settings.AWS_PUBLIC_MEDIA_LOCATION
        file_overwrite = False
    else:
        pass


class PrivateMediaStorage(S3Boto3Storage):
    if settings.DJANGO_USE_S3:
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = 'private'
        file_overwrite = False
        custom_domain = False
    else:
        pass
