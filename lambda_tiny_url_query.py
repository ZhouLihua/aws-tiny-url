import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('myTinyURL-db')


def lambda_handler(event, context):
    id = event.get("id")
    response = table.get_item(Key={'id': id})
    item = response.get("Item", None)
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
