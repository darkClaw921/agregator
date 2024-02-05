
import chromadb 

# Create a ChromaDB client
client = chromadb.Client()

# Create a collection
from chromadb.utils import embedding_functions
# collection = client.create_collection("sample_collection")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)

def add_to_collection(text,meta:dict):
    val = sentence_transformer_ef([text])
    collection = client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)
    collection.add(
        embeddings=val,
        metadatas=[meta],
        ids=[str(meta['id'])]
    )


def query(text, filter1:dict=None):
    val = sentence_transformer_ef([text])
    results = collection.query(
        query_embeddings=val,
    
        n_results=5,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter по методанным
        where=filter1, # optional filter по методанным
        # where_document={"$contains":"search_string"}  # optional filter
    )
    return results
                      
def prepare_query_chromadb(dict1:dict):
    allText=''
    metas=dict1['metadatas'][0]
    for event in metas:
        allText+=f"{event['text']}\n\n"
    return allText
# Query the collection for events on Thursday
# results = collection.query(
#     query_texts=["что в пятницу"],
#     n_results=1
# )
# print(results)
# Print the results
# for result in results:
    