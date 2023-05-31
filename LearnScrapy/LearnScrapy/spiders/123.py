from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["goodreads"]
collection = db["authorsQuotesTagsLikes"]

# Define the pipeline to remove duplicates
pipeline = [
    {
        '$group': {
            '_id': {
                'author': '$author',
                'quote_text': '$quote_text',
                'tags': '$tags',
                'likes': '$likes'
            },
            'duplicates': {'$push': '$_id'},
            'count': {'$sum': 1}
        }
    },
    {
        '$match': {
            'count': {'$gt': 1}
        }
    },
    {
        '$sort': {
            'count': -1
        }
    },
    {
        '$out': 'authorsQuotesTagsLikes'
    }
]

# Execute the pipeline to remove duplicates
collection.aggregate(pipeline)
