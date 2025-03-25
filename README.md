# GraphDB Boss

# How to use

## DB

```python
from graphdb_boss.db.client import connect

connect(db='mydb')

mydata = {
    'myid': '987192743'
    'name': 'Apple'
    'kind': 'fruit',
    'colour': 'red',
}

n = Node.upsert(mydata, ['myid'])
```

Important:
* `id` can't be used as a field (overlaps with Mongoengine's id->_id map)

## API

```python
from graphdb_boss.api.server import create
from graphdb_boss.db.client import connect

connect(db='mydb')
app = create(app_name='myapi')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
```

## ChangeStream

```python
from graphdb_boss.cs.listener import create

def example_function():
    print("Debounced function executed!")

if __name__ == '__main__':
    create(
        watched_db_name='mydb',
        watched_collection_name='mycoll',
        callback_function=example_function,
        debounce_duration=30.0
    )
```

## UI

```python
from graphdb_boss.ui.server import create

app = create(
    app_name='myui', 
    javascript_plugin_files=['C:\\Desktop\\plugin.js']
)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

```