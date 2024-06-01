import json
from datetime import datetime
import boto3


client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('parking_app_table')


def lambda_handler(event, context):
    
    checkpoint = ''
    
    try:
        # parse input
        checkpoint = 'parsing input'
        plate_id = event['queryStringParameters']['plate']
        parking_lot_id = event['queryStringParameters']['parkingLot']
        
        # calculate
        checkpoint = 'calculating'
        entry_time_server = str(datetime.now())
        ticket_id = str(plate_id) + '_' + entry_time_server
    
        # record
        checkpoint = 'recording data'
        table.put_item(
            Item={
                'id': ticket_id,
                'plate_id': plate_id,
                'parking_lot_id': parking_lot_id,
                'entry_time_server': entry_time_server
            })
        
    except: 
        body = 'Problem in ' + checkpoint
    
    else:
        body = f'Welcome from the parking app! TICKET_ID: {ticket_id}'
        
    finally:
        # output
        result = {
            'statusCode': 200,
            'body': json.dumps(body)
        }
    
    return result
    