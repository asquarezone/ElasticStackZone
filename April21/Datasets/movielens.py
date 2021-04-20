#!/usr/bin/python
import csv
import requests
import json
import sys

def create_index_ifnot_exists(index,headers={'Content-Type': "application/json"}):
    '''
    Create movie index if not exists
    '''
    # Create the movie index if it doesnot exist
    movieexists_response = requests.head(url=movie_index_url)
    if movieexists_response.status_code == 404:
        #create the index
        request_body = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 2
            },
            "mappings": {
                "properties": {
                    "year": {
                        "type": "date"
                    }
                }
            }
        }
        
        indexcreationresponse = requests.put(url=movie_index_url ,data=json.dumps(request_body), headers=headers)
        print(indexcreationresponse.status_code)
    else:
        print("movies index already exists")

def update_movies_to_index(index_url, filepath='movies.csv', headers={'Content-Type': "application/json"}):
    '''
    updated movies to the index
    '''
    with open(filepath, mode='r', encoding="utf8") as movies_file:
        movie_reader = csv.DictReader(movies_file)
        # Read the documents
        for movie in movie_reader:
            try:

                title = movie['title']
                title = title.replace('(','').replace(')','')
                year = title[-4::]
                title = title.replace(year,'').strip()
                genre_list = movie['genres'].split('|')
                moviedict = {
                    "title": title,
                    "year": year,
                    "genres": genre_list
                }
                id = movie['movieId']
                movie_json=json.dumps(moviedict)
                # index the document
                movie_doc_url=f"{index_url}/_doc/{id}"
                document_response = requests.put(url=movie_doc_url,data=movie_json, headers=headers)
                if document_response.status_code == 201:
                    print(f"Indexed a document {movie_json} with id {id}")
            except:
                print(f"Got an exception in record {movie['title']}. Skipping this record")




if __name__ == '__main__':
    '''
    This is the main method 
    '''
    elastic_search_url = "127.0.0.1"
    
    if len(sys.argv) == 2:
        elastic_search_url= sys.argv[1]
            
    movie_index_url = f"http://{elastic_search_url}:9200/movies"
    headers = {'Content-Type': "application/json"}
    create_index_ifnot_exists(movie_index_url)
    update_movies_to_index(index_url=movie_index_url, filepath='movies.csv')



