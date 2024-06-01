import json
from datetime import datetime
import boto3
import math


client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('parking_app_table')


def lambda_handler(event, context):
    
    checkpoint = ''
    
    try:
        # parse input
        checkpoint = 'parsing input'
        ticket_id = event['queryStringParameters']['ticketId']
        
        # read recorded data
        checkpoint = 'reading data'
        item = table.get_item(Key={'id': ticket_id})
        item = item["Item"]
        plate_id = item['plate_id']
        parking_lot_id = item['parking_lot_id']
        entry_time_server = datetime.fromisoformat(item['entry_time_server'])
    
        # calculate
        checkpoint = 'calculating'
        parking_time = datetime.now() - entry_time_server
        payment = math.ceil(parking_time.total_seconds() / 60.0 / 15.0) * 2.5
        
    except: 
        body = 'Problem in ' + checkpoint
    
    else:
        body = f'Welcome from the parking app! TICKET_ID: {ticket_id}'
        
    finally:
        # output
            result = {'statusCode': 200,
                'body': json.dumps(f'''Good-bye from the parking app! PLATE: {plate_id}, PARKING LOT: {parking_lot_id}, ENTRY TIME: {entry_time_server}, PARKING TIME: {parking_time}, TOTAL AMOUNT: {payment}$''')
            }
    
    return result
