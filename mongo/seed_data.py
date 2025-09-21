from mongo.db_mongo import getMongoConnection 

def run_seeders():
    print("AQUI SEEDER MONGO")
    db = getMongoConnection()
    collection = db['locations']
    collection.drop()

    """
    O tipo do indice é 2dsphere
    ele permite que o banco entenda que os dados representam pontos, linhas e polígonos 
    na superfície de uma esfera
    """
    collection.create_index([("geometry", "2dsphere")])

    docs = [
        {
            "type":"Feature",
            "name":"Hospital das Clínicas",
            "category":"hospital",
            "properties":{"city":"São Paulo", "state":"São Paulo", "country":"Brasil", "rating":4.7},
            "geometry":{"type":"Point","coordinates":[-46.6683,-23.5558]}
        },
        {
            "type":"Feature",
            "name":"Parque Ibirapuera",
            "category":"parque",
            "properties":{"city":"São Paulo", "state":"São Paulo", "country":"Brasil"},
            "geometry":{"type":"Polygon","coordinates":[[
                [-46.6606,-23.5928],[-46.6502,-23.5928],[-46.6502,-23.5850],
                [-46.6606,-23.5850],[-46.6606,-23.5928]
            ]]}
        },
        {
            "type":"Feature",
            "name":"Ciclovia Paulista",
            "category":"ciclovia",
            "properties":{"length_km":3.5, "city":"São Paulo", "state":"São Paulo", "country":"Brasil"},
            "geometry":{"type":"LineString","coordinates":[
                [-46.6820,-23.5595],[-46.6567,-23.5617],[-46.6409,-23.5654]
            ]}
        },
        {
            "type":"Feature",
            "name":"Academia Central",
            "category":"academia",
            "properties":{"city":"São Paulo", "state":"São Paulo", "country":"Brasil", "24h":True},
            "geometry":{"type":"Point","coordinates":[-46.6345,-23.5489]}
        }
    ]

    collection.insert_many(docs)