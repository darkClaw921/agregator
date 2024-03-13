
import chromadb 
from pprint import pprint

# Create a ChromaDB client
client = chromadb.Client()

# Create a collection
from chromadb.utils import embedding_functions
# collection = client.create_collection("sample_collection")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)


def add_to_collection(text,meta:dict, collectionName:str="my_collection"):
    val = sentence_transformer_ef([text])
    collection = client.get_or_create_collection(name=collectionName, embedding_function=sentence_transformer_ef)
    collection.add(
        embeddings=val,
        metadatas=[meta],
        ids=[str(meta['id'])]
    )


def query(text, filter1:dict=None, result:int=2, collectionName:str="my_collection"):
    val = sentence_transformer_ef([text])
    collection = client.get_or_create_collection(name=collectionName, embedding_function=sentence_transformer_ef)

    # is None не работает
    try:
        len(filter1)>1
    except Exception as e:
        results = collection.query(
            query_embeddings=val,
            n_results=result,)
        return results
    
    print(f'{filter1=}')
    if len(filter1)>1:
        filt={'$and':[]}
        for key, value in filter1.items():
            filt['$and'].append({key: value})        
    else:
        filt=filter1
    results = collection.query(
        query_embeddings=val,
    
        n_results=result,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter по методанным
        where=filt, # optional filter по методанным
    
        # where_document={"$contains":"search_string"}  # optional filter
    )
    return results
                      
def prepare_query_chromadb(dict1:dict)->list[dict]:
    allText=''
    dic=[]
    metas=dict1['metadatas'][0]
    distance=dict1['distances'][0]
    for event,distance1 in zip(metas, distance):
        text=event['text']
        distance=distance1
        dic.append({'text':text,'distance':distance, 
                    'theme':event['topic'],
                    'themeSearch':event['themeSearch'],
                    'hashtags':event['hashtags'],
                    'id':event['id']})
        # pprint(dic)
        # allText+=f"{event['text']}\n\n"
    return dic

def delete_collection(collectionName:str="my_collection"):
    client.delete_collection(collectionName)

# Query the collection for events on Thursday
# results = collection.query(
#     query_texts=["что в пятницу"],
#     n_results=1
# )
# print(results)
# Print the results
# for result in results:
    