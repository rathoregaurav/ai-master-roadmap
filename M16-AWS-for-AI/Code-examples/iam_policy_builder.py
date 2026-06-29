from __future__ import annotations

import json


def build_s3_read_policy(bucket_name: str) -> dict:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*",
                ],
            }
        ],
    }


def build_secrets_read_policy(secret_name: str) -> dict:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["secretsmanager:GetSecretValue"],
                "Resource": f"arn:aws:secretsmanager:*:*:secret:{secret_name}*",
            }
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_s3_read_policy("my-rag-documents"), indent=2))
    print(json.dumps(build_secrets_read_policy("openai-api-key"), indent=2))

