from pymongo import MongoClient


client = MongoClient(
    host="localhost",
    port=27017,
    username="user",
    password="pass",
    authSource="admin"
)

print(client.server_info())