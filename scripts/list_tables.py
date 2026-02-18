import boto3

dynamodb = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

response = dynamodb.list_tables()
print("Tables in DynamoDB Local:")
for table in response['TableNames']:
    print(f"  ✓ {table}")

if not response['TableNames']:
    print("  No tables found!")