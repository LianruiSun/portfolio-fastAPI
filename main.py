from fastapi import FastAPI
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve the environment variables
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

@app.post("/items/")
async def create_item(item: dict):
    table = dynamodb.Table('WPICourse')
    response = table.put_item(Item=item)
    return response

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    table = dynamodb.Table('WPICourse')
    response = table.get_item(Key={'id': item_id})
    return response.get('Item', {})

@app.get("/items/")
async def read_all_items():
    table = dynamodb.Table('WPICourse')
    response = table.scan()
    return response.get('Items', [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

