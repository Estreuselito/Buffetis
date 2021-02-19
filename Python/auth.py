# This script authenticates yourself against the AWS instance
AWS_USERNAME = "Abc"
AWS_PASSWORD = "224"

if not AWS_USERNAME and not AWS_PASSWORD:
    AWS_USERNAME = "Public"
    AWS_PASSWORD = "Public"
