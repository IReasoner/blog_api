import boto3
from config import settings
from botocore.exceptions import ClientError
from starlette.concurrency import run_in_threadpool

def _s3_get_credential():
  return boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region_name
  )


def _s3_upload_object(obj, filename):
   s3 = _s3_get_credential()
   s3.upload_fileobj(
     Fileobj=obj,
     Bucket=settings.aws_bucket_name,
     Key=f"profile_pics/{filename}",
     ExtraArgs={"ContentType": "image/jpeg"} # this stop broswer for downloading image instead of just showing some time.
   )


def _s3_delete_object(filename):
  s3 = _s3_get_credential()
  s3.delete_object(
    Bucket=settings.aws_bucket_name,
    Key=f'profile_pics/{filename}'
  )


async def upload_profile_picture(image_file, filename):
    await run_in_threadpool(_s3_upload_object, image_file, filename)


async def delete_profile_picture(filename):
  if filename is None:
    return
  
  try:
   await run_in_threadpool(_s3_delete_object, filename)
  except ClientError:
    print("Unable to delete image")

