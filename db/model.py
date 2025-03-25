from datetime import datetime, timezone
from mongoengine import DynamicDocument, DynamicEmbeddedDocument, DateTimeField, IntField, StringField, ObjectIdField, EmbeddedDocumentField


class MetadataDocument(DynamicEmbeddedDocument):
    _created_at = DateTimeField(default=datetime.now(timezone.utc))
    _updated_at = DateTimeField(default=datetime.now(timezone.utc))
    _version = IntField(default=0)

    def save(self):
        self._updated_at = datetime.now(timezone.utc)
        self._version += 1
        return super().save()


class AbstractDocument(DynamicDocument):
    meta = {'abstract': True}
    _metadata = EmbeddedDocumentField(MetadataDocument)

    def save(self, *args, **kwargs):
        if not self._metadata:
            self._metadata = MetadataDocument()
        self._metadata.save()

        return super(AbstractDocument, self).save(*args, **kwargs)


class Node(AbstractDocument):
    @staticmethod
    def upsert(doc_dict, uniqueness_fields):
        # Create a query based on the fields that can identify a unique node
        query = {field: doc_dict[field] for field in uniqueness_fields}
        n = Node.objects(**query).first()

        # If a node where the uniqueness fields match is found, update it
        if n:
            for key, value in doc_dict.items():
                setattr(n, key, value)
        # Otherwise, create a new node
        else:
            n = Node(**doc_dict)
        
        n.save()
        return n


class Edge(AbstractDocument):
    _from_node = ObjectIdField(required=True)
    _to_node = ObjectIdField(required=True)
    _name = StringField(required=True)

    @staticmethod
    def upsert(from_node, to_node, name):
        # Edge already exists?
        query = {'_from_node': from_node, '_to_node': to_node, '_name': name}
        e = Edge.objects(**query).first()

        # If not, create it
        if not e:
            e = Edge(_from_node=from_node, _to_node=to_node, _name=name)
            e.save()
        
        return e
