from __future__ import print_function  # Python 2/3 compatibility
import json
import boto3
import time
import os
import decimal


dynamodb = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')
q_name = os.environ['QUEUE_NAME']
q = sqs.get_queue_by_name(QueueName=q_name)


def trigcount(event, context):

    country = event.get('headers').get('CloudFront-Viewer-Country')
    useragent = event.get('headers').get('User-Agent')
    pageviewed = event.get('headers').get('Referer')
    requestId = event.get('requestContext').get('requestId')

    counterdata = {
        "country": country,
        "useragent": useragent,
        "pageviewed": pageviewed,
        "requestId": requestId
    }

    countertable = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    response = countertable.update_item(
        Key={
            'pageviewed': pageviewed
        },
        ExpressionAttributeNames={
            '#counter': 'counter'
        },
        ExpressionAttributeValues={
            ':i': 1
        },
        UpdateExpression='add #counter :i',
    )

    # Sending data to SQS
    send_to_sqs(json.dumps(counterdata))
    return response


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError


def send_to_sqs(data):
    q_name = os.environ['QUEUE_NAME']
    q = sqs.get_queue_by_name(QueueName=q_name)
    response = q.send_message(MessageBody=data)
    print("Got SQS MessageId back: %s" % (response.get('MessageId')))


def read_from_sqs_queue(queue):
    messages = queue.receive_messages(
        MaxNumberOfMessages=5, WaitTimeSeconds=1)
    while len(messages) > 0:
        for message in messages:
            obj = json.loads(message.body)
            update_dynamodb_02(obj["requestId"], obj["country"], obj["useragent"])
            message.delete()
        messages = queue.receive_messages(
            MaxNumberOfMessages=5, WaitTimeSeconds=1)


def process_sqs(event, context):
    read_from_sqs_queue(q)


def update_dynamodb_02(id, country, useragent):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_02'])
    response = table.put_item(
        Item={
            'id': id,
            'country': country,
            'useragent': useragent
        }
    )
