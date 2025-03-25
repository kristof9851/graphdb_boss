from mongoengine import connect as mongoengine_connect


def connect(host='127.0.0.1', port=27017, db='graphdb_boss'):
    mongoengine_connect(db, host=host, port=port)
