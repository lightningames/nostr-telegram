from pymongo import MongoClient

block_explorer= 'https://blockstream.info/'
satwatch= ""
dca = ""

currencylist = {'hkd':'$','cny': '￥','usd':'$','eur':'€'}
core_currency = "USD"


mongo_url = 'mongodb://localhost:27017'
client = MongoClient('localhost', port=27017)
# Create a new database
db = client["tgbot"] 

# db = client.tgbot
dbname = 'tgbot'

# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string



