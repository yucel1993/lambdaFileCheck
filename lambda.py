import json
import boto3
import mimetypes
import magic  # Python-magic library for accurate MIME type detection

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and object details from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Get the file from S3 (download a portion of the file)
    s3_object = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = s3_object['Body'].read(1024)  # Read the first 1KB of the file
    
    # Try to guess the MIME type using file content
    mime_detector = magic.Magic(mime=True)
    mime_type = mime_detector.from_buffer(file_content)
    
    # If MIME type is None or cannot be detected, fallback to extension
    if mime_type is None:
        mime_type, _ = mimetypes.guess_type(object_key)
    
    print(f"Detected MIME type: {mime_type}")
    
    # Define the folder structure based on MIME type (create folders based on the MIME type category)
    if mime_type:
        main_type = mime_type.split('/')[0]  # Get the primary type (e.g., image, audio, video)
        folder_name = f"{main_type}_files/"
    else:
        folder_name = "unknown_files/"
    
    # Define new S3 object key within the appropriate folder
    new_object_key = folder_name + object_key.split('/')[-1]
    
    # Copy the file to the new folder in S3
    s3.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key},
        Key=new_object_key
    )
    
    # Delete the original file from the root
    s3.delete_object(Bucket=bucket_name, Key=object_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"File moved to {folder_name}")
    }
