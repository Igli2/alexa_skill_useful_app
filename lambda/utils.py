import logging
import os
import boto3
from botocore.exceptions import ClientError

def update_session_attributes(handler_input, attribute, value):
    handler_input.attributes_manager.session_attributes[attribute] = value

def get_session_attribute(handler_input, attribute):
    session_attributes = handler_input.attributes_manager.session_attributes
    if attribute in session_attributes:
        return session_attributes[attribute]
    else:
        return None

def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response