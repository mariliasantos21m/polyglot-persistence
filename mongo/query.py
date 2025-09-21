from mongo.db_mongo import getMongoConnection
from dtos.location import Location

def serialize(doc):
    """
    Serializa um documento retornado pelo cursor do PyMongo para que seja JSON-serializável.

    Substitui o campo "_id" do MongoDB por "id" como string e mantém os demais campos inalterados.

    Args:
        doc (dict): Documento retornado pelo cursor do PyMongo.

    Returns:
        dict: Documento serializado pronto para ser retornado pelo FastAPI.
    """
    doc = doc.copy()  # evita modificar o documento original
    doc["id"] = str(doc.pop("_id"))
    return doc

def get_locations(params):
    db = getMongoConnection()
    if db is None: return []

    query = {}

    if params["city"]:
        query["properties.city"] = {"$in": params["city"]}
    if params["state"]:
        query["properties.state"] = {"$in": params["state"]}
    if params["country"]:
        query["properties.country"] = {"$in": params["country"]}

    print("query", query)
    cursor= db.locations.find(query)
    return [serialize(d) for d in cursor]

def create_location(location: Location):
    db = getMongoConnection()

    feature = {
        "name": location.name,
        "category": location.category,
        "properties": location.properties,
        "geometry": location.geometry.model_dump(),
    }
    
    res= db.locations.insert_one(feature)
    feature["_id"] = res.inserted_id
    return serialize(feature)
