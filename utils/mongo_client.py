from pymongo import MongoClient, errors
import time


class AwesomDBClient(MongoClient):
    def __init__(self, url):
        super().__init__(url)
        # create db if it does not exist
        self.db = self['awesome']
        self.profile_collection = self.db['profiles']
        self.profile_collection.create_index('username', unique=True, background=True)
        self.message_collection = self.db['messages']
        self.chat_collection = self.db['chats']
        self.chat_collection.create_index('chat', unique=True, background=True)
        self.add_profile({'username': 'Nastya', 'password': '1111'})
        self.add_profile({'username': 'Oleg', 'password': '2222'})
        self.add_profile({'username': 'Cat', 'password': '3'})
        self.add_chat({'chat': 'ALL', 'userlist': []})
        self.add_users_to_chat('ALL', 'Nastya', 'Oleg', 'Cat')

    def add_profile(self, doc):
        if not 'username' in doc or not 'password' in doc:
            return {'result': 'error', 'msg': 'must contain fields: username, password'}
        doc['timestamp'] = time.time()
        try:
            self.profile_collection.insert_one(doc)
            return {'result': 'ok'}
        except errors.DuplicateKeyError:
            return {'result': 'error', 'msg': 'profile {} already exists'.format(doc['username'])}

    def add_message(self, doc):
        if not 'msg' in doc or not 'from' in doc or not 'to' in doc:
            return {'result': 'error', 'msg': 'must contain fields: message, from, to'}
        doc['timestamp'] = time.time()
        self.message_collection.insert_one(doc)
        return {'result': 'ok'}

    def add_chat(self, doc):
        if not 'chat' in doc or not 'userlist' in doc:
            return {'result': 'error', 'msg': 'must contain fields: chat, userlist'}
        doc['timestamp'] = time.time()
        try:
            self.chat_collection.insert_one(doc)
            return {'result': 'ok'}
        except errors.DuplicateKeyError:
            return {'result': 'error', 'msg': 'chat {} already exists'.format(doc['chat'])}

    def add_users_to_chat(self, chat, *usernames):
        c = self.chat_collection.find({'chat': chat})
        if not c:
            return {'result': 'error', 'msg': 'chat {} does not exist'.format(chat)}
        for username in usernames:
            user = self.profile_collection.find_one({'username': username})
            if user and c:
                self.chat_collection.update_one({'chat': chat}, {'$addToSet': {'userlist': user['_id']}})
        return {'result': 'ok'}

    def get_chats(self):
        chats = {}
        for x in self.chat_collection.find():
            current_chat = x['chat']
            chat_users = []
            for u in x['userlist']:
                current_user = self.profile_collection.find_one({'_id': u})
                chat_users.append(current_user['username'])
            chats[current_chat] = chat_users
        return chats

    def get_profile(self, username):
        x = self.profile_collection.find_one({'username': username})
        if x:
            return {'username': x['username'], 'password': x['password']}
        else:
            return None



if __name__ == '__main__':
    # db initialization
    mongo_client = AwesomDBClient('mongodb://localhost:27017/')
    # list current data in db
    print('---profile_collection---')
    for x in mongo_client.profile_collection.find():
        print(x['_id'])
    print('---chat_collection---')
    x = mongo_client.get_chats()
    print(x)
    print('---message_collection---')
    for x in mongo_client.message_collection.find():
        print(x)
    x = mongo_client.get_profile('Nastya')
    print(x)
    x = mongo_client.get_profile('nastya')
    print(x)
