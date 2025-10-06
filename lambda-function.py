import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    try:
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        message = body['message']
    except:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid request'})
        }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ContactFormSubmissions')
    
    try:
        table.put_item(Item={
            'id': str(datetime.now().timestamp()),
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
