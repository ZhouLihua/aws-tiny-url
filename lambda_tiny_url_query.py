import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('myTinyURL-db')

ENDPOINT="https://7rqjxtzse9.execute-api.us-east-1.amazonaws.com/prod"

# opposite of generate_short_uri
def decode_short_url(short_url):
    bits = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    uid = 0
    length = len(short_url)
    for key, val in enumerate(short_url):
        index = bits.index(val)
        uid += index * pow(62, length - key - 1)
    return uid


def lambda_handler(event, context):
    queryParams = event.get("pathParameters")
    shortUrl = queryParams.get("shortUrl")
    uuid = decode_short_url(shortUrl)
    response = table.get_item(Key={'id': uuid})
    item = response.get("Item", None)
    if item:
        return {
            'statusCode': 301,
            'headers':{
                "Location": item.get("longUrl")
            }
        }
    else:
        return {
            'statusCode': 404,
            'body': "can not found longurl for %s" % shortUrl
        }
