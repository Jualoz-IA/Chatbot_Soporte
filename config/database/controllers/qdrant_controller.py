from qdrant_client import QdrantClient
import os

client = QdrantClient(
    url=os.getenv("QDRANT_DATABASE_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def table_collections():
    collections = get_collections()
    table = []
    for collection in collections.collections:
        c = get_collection_name(collection.name)
        table.append({
            "Nombre": collection.name,
            "Tamaño": c.config.params.vectors.size,
            "Métrica": c.config.params.vectors.distance
        })
    return table

def get_names_collections():
    collections = get_collections()
    names = []
    for collection in collections.collections:
        names.append(collection.name)
    return names
        

def get_collections():
    collections = client.get_collections()
    return collections

def get_collection_name(name):
    collection = client.get_collection(name)
    return collection

def delete_collection(collection_name):
    client.delete_collection(collection_name)

def recreate(name, size, distance):
    client.recreate_collection(
        collection_name=name,
        vectors_config={"size": size, "distance": distance}
    )
        