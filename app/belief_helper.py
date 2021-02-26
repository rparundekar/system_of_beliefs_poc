import os
import hashlib
import tempfile
import traceback
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from datetime import timedelta

minio_client = Minio(os.getenv('S3_URL'),
                access_key=os.getenv('S3_ACCESS_KEY'),
                secret_key=os.getenv('S3_SECRET_KEY'),
                region=os.getenv('S3_REGION_NAME'),
                secure=(os.getenv('S3_SECURE', "false")=="true"))

BELIEF_BUCKET = os.getenv('S3_BUCKET_NAME')

def validate(belief_text):
    lines = belief_text.splitlines()
    if len(lines) < 4: return f"Belief document seems incomplete. It needs to have the belief identifier, at least one claim, believer's identifier, and believer's signature on new lines - currently the document only has {len(lines)} lines.", None, None, None, None
    
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
    m = hashlib.md5()
    m.update(belief_id.encode("utf-8"))
    belief_id_hash = m.hexdigest()
    key = f"{belief_id_hash}.belief"
    try:
        with tempfile.NamedTemporaryFile(suffix='.belief') as ntf:
            with open(ntf.name, "w") as f:
                f.write(belief_text)
            minio_client.fput_object(BELIEF_BUCKET, key, ntf.name)
    except Exception as e:
        traceback.print_exc()
        return f"{e}"

    return None

def get_belief(belief_id):
    # get s3 location of the belief
    m = hashlib.md5()
    m.update(belief_id.encode("utf-8"))
    belief_id_hash = m.hexdigest()
    key = f"{belief_id_hash}.belief"
    try:
        presigned_url = minio_client.presigned_get_object(BELIEF_BUCKET, key, expires=timedelta(hours=2))
        return None, presigned_url
    except Exception as e:
        traceback.print_exc()
        return f"{e}", None


    
