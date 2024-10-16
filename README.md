
# AWS Lambda S3 File Handler

This project implements an AWS Lambda function that processes files uploaded to an S3 bucket. The Lambda function detects the MIME type of the uploaded files and organizes them into specific folders based on their type.

### Project Setup
- Replace `<your-bucket-name>` with the actual name of your S3 bucket in the IAM policy sections.
- in this repo, do `mkdir python`
- execute following 
```
pip install python-magic -t python/
pip install libmagic -t python/
```
Zip everything (both the python/ directory and lambda.py)
```
zip -r lambda-magic.zip python/ lambda.py
```
Go to the lamda function and upload from zip file
Upload and select your lambda-magic.zip file

### Lambda Role
I am Role for lamda to execute S3
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:CopyObject"
            ],
            "Resource": "arn:aws:s3:::<your-bucket-name>/*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:*",
            "Resource": "*"
        }
    ]
}

```
### S3 Role
I am role for S3 to invoke lambda

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:DeleteObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*"
        }
    ]
}

```
