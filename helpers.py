import pandas as pd
import numpy as np
import warnings
import openai
import time
warnings.filterwarnings("ignore")

def load_data(data_path):
    character_metadata = pd.read_csv(data_path + 'MovieSummaries/character.metadata.tsv', 
                                 sep='\t', 
                                 names= [
                                     'Wikipedia movie ID',
                                     'Freebase movie ID',
                                     'Movie release date',
                                     'Character name',
                                     'Actor date of birth',
                                     'Actor gender',
                                     'Actor height (in meters)',
                                     'Actor ethnicity (Freebase ID)',
                                     'Actor name',
                                     'Actor age at movie release',
                                     'Freebase character/actor map ID',
                                     'Freebase character ID',
                                     'Freebase actor ID'
                                 ]
                                 )

    movie_metadata = pd.read_csv(data_path + 'MovieSummaries/movie.metadata.tsv', sep='\t', header=0,
                             names=['Wikipedia movie ID',
                                         'Freebase movie ID',
                                         'Movie name',
                                         'Movie release date',
                                         'Movie box office revenue',
                                         'Movie runtime',
                                         'Movie languages (Freebase ID:name tuples)',
                                         'Movie countries (Freebase ID:name tuples)',
                                         'Movie genres (Freebase ID:name tuples)'
                                         ])

    plot_summaries = pd.read_csv(data_path + 'MovieSummaries/plot_summaries.txt', sep='\t', names=[
        'Wikipedia movie ID',
        'Summary'
    ])
    
    # load the embeddings from disk
    embeddings = np.load(data_path + 'embeddings.npy', allow_pickle=True)
    embeddings_df = pd.DataFrame(embeddings, columns=['Wikipedia movie ID', 'embedding'])
    
    # Combine on the first column of embeddings
    combined_plot_summaries = pd.merge(plot_summaries, embeddings_df, on='Wikipedia movie ID')
    
    embeddings = np.array(embeddings[:,1].tolist())
    
    return {
        'character_metadata': character_metadata,
        'movie_metadata': movie_metadata,
        'plot_summaries': plot_summaries,
        'embeddings': embeddings,
        'combined_plot_summaries': combined_plot_summaries
    }
    
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    text = text.replace("\x0b", " ")
    text = text.replace("\x0c", " ")
    try:
        embedding = openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

        if embedding is None:
            print(f"Failed to process text: {text}. Error: embedding is None")
            return None
        return embedding
    except openai.error.OpenAIError as e:
        print(f"Failed to process text: {text}. Error: {str(e)}")
        time.sleep(60)
        return None