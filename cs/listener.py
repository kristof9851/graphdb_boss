import threading
import time
from mongoengine import connection
from graphdb_boss.db.client import connect
from graphdb_boss.db.model import Node

# mongodb convert-standalone-to-replica-set


class ChangeStreamListener:
    def __init(self, db_name, collection_name, debounced_fn, debounce_duration=5.0):
        self.db_name = db_name
        self.collection_name = collection_name
        self.debounced_fn = debounced_fn
        self.debounce_duration = debounce_duration
        
        self.debounce_timer = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.listener_thread = threading.Thread(target=self._listener)

    def _debounce(self):
        with self.lock:
            if self.debounce_timer is not None:
                self.debounce_timer.cancel()
            
            self.debounce_timer = threading.Timer(self.debounce_duration, self.debounced_fn)
            self.debounce_timer.start()

    def _listener(self):
        mongo_client = connection.get_connection()
        mongo_db = mongo_client[self.db_name]
        mongo_collection = mongo_db[self.collection_name]

        with mongo_collection.watch() as stream:
            for change in stream:
                if self.stop_event.is_set():
                    print(f'Stopping listener for collection: {self.collection_name}...')
                    break

                print(f'Change detected in collection: {self.collection_name}: ', change)

                self._debounce()

    def start(self):
        self.listener_thread.start()

    def stop(self):
        self.stop_event.set()
        self.listener_thread.join()


def create(watched_db_name, watched_collection_name, callback_function, debounce_duration):
    connect(db=watched_db_name)

    listener = ChangeStreamListener(
        db_name=watched_db_name, 
        collection_name=watched_collection_name, 
        debounced_fn=callback_function, 
        debounce_duration=debounce_duration
    )

    try:
        listener.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCtrl+C detected! Stopping listener...")
        listener.stop()
