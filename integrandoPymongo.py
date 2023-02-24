import pprint

client = []
db = client.test
collection = db.test_collection

post = {
    "Nome":"Leonardo",
    "cpf":"4343434343",
    "endereco": "dadadad",
    "conta": {
        "tipo": "corrente",
        "agencia": "dadd",
        "num": 32,
        "saldo": 3233
        },
    }

posts = db.pots
post_id = posts.insert_one(post).inserted_id
print(post_id)

pprint.pprint(db.posts.find_one())
new_post = [{
    "Nome":"Leonardo",
    "cpf":"4343434343",
    "endereco": "dadadad",
    "conta": {
        "tipo": "corrente",
        "agencia": "dadd",
        "num": 32,
        "saldo": 3233
        },
    },
    {
        "Nome":"Leonardo",
        "cpf":"4343434343",
        "endereco": "dadadad",
        "conta": {
            "tipo": "corrente",
            "agencia": "dadd",
            "num": 32,
            "saldo": 3233
        },
    }]

result = posts.insert_many(new_post)
print(result.inserted_ids)

pprint.pprint(db.posts.find_one({"Nome": "Leonardo"}))

print("\n Documentos presentes em posts")
for post in posts.find():
    pprint.pprint(post)

print(post.count_documents({"Nome":"Leonardo"}))

print("\n Documentos presentes em posts de maneira ordenada")
for post in posts.find({}).sort("Nome"):
    pprint.pprint(post)