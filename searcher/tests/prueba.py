from header import *
from triplet import TripletBuilder

root = ROOT

vars = ConfigVariables(root)
env_var = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD', 'CA_CERT', 'OPENAI_API_KEY')
cert_mod = root + env_var['CA_CERT']
env_var['CA_CERT'] = cert_mod
clients = Clients(**env_var)
builder = TripletBuilder()

chunks = clients.elastic_search().search(index='goodfellas-chunk', size=20)

triplets = builder.chunk_to_triplets(clients.open_ai(), 'gpt-3.5-turbo', chunks)

print(triplets.model_dump_json(indent=2))

with open('../../triplets.json', 'w') as f:
    f.write(triplets.model_dump_json(indent=2))
