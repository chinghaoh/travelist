import boto3
from django.conf import settings

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

def upload_photo(file,key):
    client = get_s3_client()
    client.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        key,
        ExtraArgs={'ContentType': file.content_type}
    )
    return key

def get_presigned_url(key,expiry=3600):
    client = get_s3_client()
    url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': key,
        },
        ExpiresIn=expiry
    )
    return url

def delete_photo(key):
    client = get_s3_client()
    client.delete_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
    )