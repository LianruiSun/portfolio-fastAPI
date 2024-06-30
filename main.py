from fastapi import FastAPI
import boto3
from dotenv import load_dotenv
import os
from mangum import Mangum

load_dotenv()

ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
REGION_NAME = os.getenv('REGION_NAME')

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    region_name=REGION_NAME
)

app = FastAPI()
handler = Mangum(app)

@app.get("/{item_id}")
async def read_item(item_id: str):
    table = dynamodb.Table('WPICourse')
    response = table.get_item(Key={'id': item_id})
    return response.get('Item', {})

@app.get("/")
async def read_all_items():
    table = dynamodb.Table('WPICourse')
    response = table.scan()
    return response.get('Items', [])