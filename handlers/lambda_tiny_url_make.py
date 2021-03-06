import boto3
import time
import json


# db schema
# partition key: id, type number
# attribute: longUrl, type string
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('myTinyURL-db')


ENDPOINT="https://7rqjxtzse9.execute-api.us-east-1.amazonaws.com/prod/"

# for each make request, we should assume a unique id for it, and
# generate a short url for it. base62 algoritm
def generate_short_url(uuid):
    bits = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortURL = ""
    # for each digit find the base 62
    while uuid > 0:
        shortURL += bits[uuid % 62]
        uuid /= 62
    return shortURL[:: -1]


def lambda_handler(event, context):
    body = event.get("body")
    bodyJson = json.loads(body)
    longUrl = bodyJson.get("longUrl")
    uid = int(time.time())
    shortUrl = generate_short_url(uid)

    table.put_item(
        Item={
            'id': uid,
            'longUrl': longUrl
        }
    )

    response = {
        "shortUrl": ENDPOINT + shortUrl
    }
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(response)
    }
