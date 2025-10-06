import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        message = body['message']
    except:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
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
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Success'})
        }
    except:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Failed to save'})
        }
