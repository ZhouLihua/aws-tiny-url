import boto3
import time


# db schema
# partition key: id, type number
# attribute: longUrl, type string
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('myTinyURL-db')


def lambda_handler(event, context):
    longUrl = event.get("longUrl")
    id = int(time.time())
    table.put_item(
        Item={
            'id': id,
            'longUrl': longUrl
        }
    )

    return {
        'statusCode': 200,
        'body': id
    }
