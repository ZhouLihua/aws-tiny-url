import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('myTinyURL-db')


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
    shortUrl = event.get("shortUrl")
    uuid = decode_short_url(shortUrl)
    response = table.get_item(Key={'id': uuid})
    item = response.get("Item", None)
    item["shortUrl"] = shortUrl
    if item:
        return {
            'statusCode': 200,
            'body': item
        }
    else:
        return {
            'statusCode': 404,
            'body': "item not found"
        }
