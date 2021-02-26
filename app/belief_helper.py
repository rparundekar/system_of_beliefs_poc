import os
import hashlib
from minio import Minio

minio_client = Minio(os.getenv('S3_URL'),
                access_key=os.getenv('S3_KEY_ID'),
                secret_key=os.getenv('S3_SECRET_KEY'),
                region=os.getenv('S3_REGION_NAME'),
                secure=(os.getenv('S3_SECURE', "false")=="true"))

BELIEF_BUCKET = os.getenv('BELIEF_BUCKET')

def validate(belief_text):
    lines = belief_text.splitlines()
    if len(lines) < 4: return f"Belief document seems incomplete. Needs atleast the belief identifier, at least one claim, believer's identifier, and believer's signature on new lines - currently the document only has {len(lines)} lines."
    
    belief_id = lines[0]
    # TODO: validate belief id

    entity_id = lines[-2]
    # TODO: validate entity_id

    signature = lines[-1]
    # TODO: validate signature

    claims = lines[1:len(lines)-2]
    # TODO: validate claims

    return None, belief_id, entity_id, signature, claims
    
def remember_belief(belief_id, belief_text):
    # get s3 location of the belief
    belief_id_hash = hashlib.md5().update(belief_id).hexdigest()
    key = f"{belief_id_hash}.belief"
    minio_client.put_object(BELIEF_BUCKET, key, belief_text)
    return None

def get_belief(belief_id):
    # get s3 location of the belief
    belief_id_hash = hashlib.md5().update(belief_id).hexdigest()
    key = f"{belief_id_hash}.belief"
    presigned_url = client.presigned_get_object(BELIEF_BUCKET, key, expires=timedelta(hours=2))
    return presigned_url


    
