from pymongo import MongoClient, DESCENDING, ASCENDING
import datetime as dt
import logging
from logging import handlers
from bson.objectid import ObjectId
from constants import db, dbname

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger(dbname).setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

posts = db.posts

# get count of posts by user id
def get_count(username):
    try:
        num_offers = posts.count_documents({'username': username})
        return num_offers
    except Exception as e:
        logger.error(e)
        return -1


def delete_alldocs_by_user(username):
    try:
        result = posts.delete_many({'username': username})
        count = result.deleted_count
        return count
    except Exception as e:
        logger.error(e)
        return -1


def delete_entry(username, id):
    try:
        result = posts.delete_one({'username': username, '_id': ObjectId(id)})
        count = result.deleted_count
        print(f'Delete_Entry total deleted: {count}')
        return count
    except Exception as e:
        logger.error(e)
        return -1


def find_by_id(id):
    try:
        update = posts.find({'_id': ObjectId(id)})
        return update
    except Exception as e:
        logger.error(e)
        return -1


def find_active_offers(username):
    try:
        result = posts.find({'active': {"$eq": True}, 'username': username})
        return result
    except Exception as e: 
        logger.error(e)
        return -1
    
def find_all_offers():
    try:
        result = posts.find({'active': {"$eq": True}})
        return result
    except Exception as e: 
        logger.error(e)
        return -1

def parse_offers(result):
    s = ''
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    for r in result:
        postdate = r['initdate'].strftime(fmt)
        id =str(r['_id'])
        s = s + "Offer: " + r['offer'] + "\n"
        s = s + "By: @" + r['username'] + "\n"
        s = s + "Date: " + postdate + "\n"
        s = s + "ID: " + id + "\n\n"
    return s
    

def add_doc(post_one):
    # add a document
    try:
        result = posts.insert_one(post_one)
        logger.info('One post: {0}'.format(result.inserted_id))
        return result.inserted_id
    except Exception as e:
        logger.error(e)
        return -1


def drop_bulk_db(pattern2drop):
    # example: pattern2drop == 'intro-mongodb-testing"
    try:
        dbnames = client.list_database_names()
        for each in dbnames:
            if pattern2drop in each:
                logger.info(each)
                client.drop_database(each, session=None)
    except Exception as e:
        logger.error(e)


# example post
post_one = {
    'username': 'joetest',
    'offer': 'Buy 0.05 btc, %Kraken FPS/ATM/Cash',
    'active' : True,
    'initdate': dt.datetime.now()
}

post_two = {
    'username': 'samtest',
    'offer': 'Sell 0.02 btc, %Coinbase FPS/ATM/Cash',
    'active' : True,
    'initdate': dt.datetime.now()
}

post_three = {
    'username': 'samtest',
    'offer': 'Sell 0.03 btc, %bitstamp FPS/ATM/Cash',
    'active' : True,
    'initdate': dt.datetime.now()
}


def add_examples():
    print("adding one test post")
    result = add_doc(post_one)
    if result != -1:
        print(f'post id: {result}')
    else: 
        print(f'Error with post - please contact an admin')

    print("adding two test post: ")
    id_result = add_doc(post_two)
    print(f'post id: {id_result}')

    print("adding three test post: ")
    result3 = add_doc(post_three)
    print(f'post id: {result3}')

    usertwo = post_two['username']
    two_count = get_count(usertwo)
    print(f'count total for {usertwo} : {two_count}')   

    userone = post_one['username']
    one_count = get_count(userone)
    print(f'count total for {userone} : {one_count}')   

    result = find_by_id(id_result)
    response  = parse_offers(result)    
    print(f'\nResult from Find by Id: \n {response} ')

    print(f'delete one id: {id_result}')
    count = delete_entry(usertwo, id_result)
    print(f'total deleted: {count}\n')


if __name__ == "__main__":
    
    # real simple 'unit' test
    drop_bulk_db(dbname)
    add_examples()

    usertwo = post_two['username']    
    userone = post_one['username']
    
    result = find_active_offers(usertwo)
    offers = parse_offers(result)
    print(f'\nAll open offers from {usertwo}:\n {offers}')
    print("=========")
    
    result = find_all_offers()
    offers = parse_offers(result)
    print(f'All open offers from All Users: {offers}')
    
    id = "5fd097c1f9b86b2dd68be68a" # example id
    print(f'delete one id: {id}')
    count = delete_entry('samtest', id)
    print(f'total deleted: {count} \n')
     
    print(f'delete all docs by user: {userone} ')
    result = delete_alldocs_by_user(userone)
    print(result)
    
    print(f'delete all docs by user: {usertwo} ')
    result = delete_alldocs_by_user(usertwo)
    print(result)
   
