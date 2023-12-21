##############################################
# This file contains all the helper functions
# that we use in the notebook
##############################################

import pandas as pd
import numpy as np
import warnings
from openai import OpenAI
import time
import json
warnings.filterwarnings("ignore")

def load_city_country_analysis(combined_plot_summaries, data_path):
    # We load from movie_analysis.json and convert to df
    with open(data_path + '/movie_analysis.json', 'r') as f:
        analysis = json.load(f)
    
    # We convert the string in the values to a dict
    for key, value in analysis.items():
        analysis[key] = json.loads(value)
    
    def get_cities(one_analysis):
        if one_analysis is None:
            return []

        if 'cities' not in one_analysis:
            return []

        return one_analysis['cities']

    cities = [get_cities(value) for _, value in analysis.items()]
    cities = sorted(list(set([item for sublist in cities for item in sublist])))

    def get_countries(one_analysis):
        if one_analysis is None:
            return []

        if 'countries' not in one_analysis:
            return []

        return one_analysis['countries']

    countries = [get_countries(value) for _, value in analysis.items()]
    countries = sorted(list(set([item for sublist in countries for item in sublist])))
    
    cities_movies = {city: [] for city in cities}
    countries_movies = {country: [] for country in countries}

    for key, value in analysis.items():
        movie_cities = get_cities(value)
        movie_countries = get_countries(value)

        for city in movie_cities:
            if city in cities_movies:
                cities_movies[city].append(int(key))

        for country in movie_countries:
            if country in countries_movies:
                countries_movies[country].append(int(key))
                
    
    # Remove all countries with less than 10 movies both from countries and countries_movies
    countries = [country for country in countries if len(countries_movies[country]) >= 10]
    countries_movies = {country: countries_movies[country] for country in countries}
    
    # Remove all cities with less than 10 movies both from cities and cities_movies
    cities = [city for city in cities if len(cities_movies[city]) >= 10]
    cities_movies = {city: cities_movies[city] for city in cities}
    
    # These are corrections to the errors that ChatGPT made
    broken_countries = ['unknown', 'unspecified', 'None', 'Moon', '', 'Africa', 'fictional', 'Unknown', 'Earth', 'Mars', 'South America']
    broken_cities = ['unknown', 'unspecified', 'None', 'Moon', '', 'village', 'town', 'small village', 'small town', 'remote village', 'hospital', 'fishing village', 'desert', 'countryside', 'city', 'big city', 'Unnamed City', 'Unknown', 'Town', 'Times Square',  'Small Town', 'Small town',  'Paradise',
                     'Gotham City', 'Europe', 'Earth', 'City', 'Atlantic City', 'Metropolis', 'Brooklyn', 'Hollywood', 'Manhattan', 'California']

    countries_in_cities = ['Russia', 'Australia', 'Canada', 'United States', 'India', 'Iraq', 'New Zealand', 'Mexico', 'Jamaica', 'Japan', 'Italy', 'Panama', 'Rome', 'Singapore', 'Switzerland', 'Sweden', 'Spain','Germany', 'England', 'Egypt', 'China', 'Alexandria', 'America', 'France', 'Holland', 'Brazil', 'Vietnam', 'Greece', 'Thailand']
    cities_to_merge = [
        ['Washington D.C.', 'Washington', 'Washington DC', 'Washington, D.C.', 'Washington, DC'],
        ['Texas', 'Texas town'],
        ['New York', 'New York City'],
    ]
    
    countries_to_merge = [
        ['United Kingdom', 'England', 'UK', 'Great Britain', 'Northern Ireland', 'Wales', 'Scotland'],
        ['Myanmar', 'Burma'],
        ['Egypt', 'Alexandria'],
        ['Netherlands', 'Holland'],
        ['Italy', 'Rome'],
        ['Bosnia and Herzegovina', 'Bosnia'],
        ['United States', 'America', 'USA'],
        ['USSR', 'Soviet Union']
    ]


    # We will now remove all the broken countries and cities
    for country in broken_countries:
        if country in countries:
            countries.remove(country)
            del countries_movies[country]

    for city in broken_cities:
        if city in cities:
            cities.remove(city)
            del cities_movies[city]

    # We will now merge the cities that are in countries
    for country in countries_in_cities:
        if country in cities:
            if country not in countries:
                countries += [country]
                countries_movies[country] = []
            countries_movies[country] += cities_movies[country]
            countries_movies[country] = list(set(countries_movies[country]))
            del cities_movies[country]
            cities.remove(country)

    # We will now merge the cities that are in cities_to_merge
    for cities_to_merge_list in cities_to_merge:
        if cities_to_merge_list[0] in cities:
            for city in cities_to_merge_list[1:]:
                if city in cities:
                    cities_movies[cities_to_merge_list[0]] += cities_movies[city]
                    cities_movies[cities_to_merge_list[0]] = list(set(cities_movies[cities_to_merge_list[0]]))
                    del cities_movies[city]
                    cities.remove(city)
                    
    # We will now merge the countries that are in countries_to_merge
    for countries_to_merge_list in countries_to_merge:
        if countries_to_merge_list[0] in countries:
            for country in countries_to_merge_list[1:]:
                if country in countries:
                    countries_movies[countries_to_merge_list[0]] += countries_movies[country]
                    countries_movies[countries_to_merge_list[0]] = list(set(countries_movies[countries_to_merge_list[0]]))
                    del countries_movies[country]
                    countries.remove(country)


    # We get and aggregate the embeddings of the movies in the cities and countries
    embeddings_of_movies_in_cities = { city: [] for city in cities }
    embeddings_of_movies_in_countries = { country: [] for country in countries }

    for city_country in cities:
        embeddings_of_movies_in_cities[city_country] = np.array(combined_plot_summaries.loc[combined_plot_summaries['Wikipedia movie ID'].isin(cities_movies[city_country])]['embedding'].values.tolist())
    
    for city_country in countries:
        embeddings_of_movies_in_countries[city_country] = np.array(combined_plot_summaries.loc[combined_plot_summaries['Wikipedia movie ID'].isin(countries_movies[city_country])]['embedding'].values.tolist())

    # We return this as a dict
    return {
        'cities': cities,
        'countries': countries,
        'cities_movies': cities_movies,
        'countries_movies': countries_movies,
        'embeddings_of_movies_in_cities': embeddings_of_movies_in_cities,
        'embeddings_of_movies_in_countries': embeddings_of_movies_in_countries
    }
    
    
    
def load_data(data_path):
    """
    Does all data loading and preprocessing
    """
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
    
    # We load the city and country analysis
    city_country_analysis = load_city_country_analysis(combined_plot_summaries, data_path)

    cities_in_country = {
    'Afghanistan': ['Kabul'],
    'Albania': ['Tirana'],
    'Algeria': ['Algiers'],
    'Argentina': ['Buenos Aires'],
    'Australia': ['Adelaide', 'Brisbane', 'Melbourne', 'Perth', 'Sydney'],
    'Austria': ['Vienna'],
    'Bahamas': ['Nassau'],
    'Bangladesh': ['Dhaka'],
    'Belgium': ['Brussels'],
    'Bolivia': ['La Paz', 'Sucre'],
    'Bosnia and Herzegovina': ['Sarajevo'],
    'Brazil': ['Brasília', 'Rio de Janeiro', 'São Paulo'],
    'Britain': ['London'],
    'Bulgaria': ['Sofia'],
    'Burkina Faso': ['Ouagadougou'],
    'Burma': ['Naypyidaw'],
    'Cambodia': ['Phnom Penh'],
    'Cameroon': ['Yaoundé'],
    'Canada': ['Ottawa', 'Toronto', 'Vancouver'],
    'Chile': ['Santiago'],
    'China': ['Beijing', 'Hong Kong', 'Shanghai', 'Taipei'],
    'Colombia': ['Bogotá'],
    'Congo': ['Kinshasa'],
    'Costa Rica': ['San José'],
    'Croatia': ['Zagreb'],
    'Cuba': ['Havana'],
    'Czech Republic': ['Prague'],
    'Denmark': ['Copenhagen'],
    'Dominican Republic': ['Santo Domingo'],
    'Egypt': ['Cairo'],
    'El Salvador': ['San Salvador'],
    'Estonia': ['Tallinn'],
    'Ethiopia': ['Addis Ababa'],
    'Finland': ['Helsinki'],
    'France': ['Cannes', 'Marseille', 'Nice', 'Paris'],
    'Georgia': ['Tbilisi'],
    'Germany': ['Berlin', 'Frankfurt', 'Munich'],
    'Greece': ['Athens'],
    'Hong Kong': ['Hong Kong'],
    'Hungary': ['Budapest'],
    'Iceland': ['Reykjavik'],
    'India': ['Bangalore', 'Bombay', 'Calcutta', 'Chandigarh', 'Chennai', 'Cochin', 'Coimbatore', 'Delhi', 'Hyderabad', 'Kochi', 'Kolkata', 'Lucknow', 'Madras', 'Mangalore', 'Mumbai', 'Ooty', 'Pondicherry', 'Pune', 'Rajasthan'],
    'Indonesia': ['Jakarta'],
    'Iran': ['Tehran'],
    'Iraq': ['Baghdad'],
    'Ireland': ['Dublin'],
    'Israel': ['Jerusalem', 'Tel Aviv'],
    'Italy': ['Florence', 'Milan', 'Palermo', 'Rome', 'Sicily', 'Turin', 'Tuscany', 'Venice'],
    'Jamaica': ['Kingston'],
    'Japan': ['Hiroshima', 'Kyoto', 'Osaka', 'Tokyo', 'Yokohama'],
    'Jordan': ['Amman'],
    'Kenya': ['Nairobi'],
    'Korea': ['Seoul'],
    'Kuwait': ['Kuwait City'],
    'Lebanon': ['Beirut'],
    'Libya': ['Tripoli'],
    'Lithuania': ['Vilnius'],
    'Malaysia': ['Kuala Lumpur'],
    'Mali': ['Bamako'],
    'Malta': ['Valletta'],
    'Mauritius': ['Port Louis'],
    'Mexico': ['Acapulco', 'Tijuana', 'Mexico City'],
    'Monaco': ['Monaco'],
    'Mongolia': ['Ulaanbaatar'],
    'Morocco': ['Rabat', 'Casablanca'],
    'Mozambique': ['Maputo'],
    'Myanmar': ['Naypyidaw'],
    'Nepal': ['Kathmandu'],
    'Netherlands': ['Amsterdam'],
    'New Zealand': ['Wellington', 'Auckland'],
    'Niger': ['Niamey'],
    'Nigeria': ['Abuja'],
    'Norway': ['Oslo'],
    'Pakistan': ['Islamabad', 'Karachi'],
    'Panama': ['Panama City'],
    'Papua New Guinea': ['Port Moresby'],
    'Peru': ['Lima'],
    'Philippines': ['Manila'],
    'Poland': ['Warsaw'],
    'Portugal': ['Lisbon'],
    'Puerto Rico': ['San Juan'],
    'Romania': ['Bucharest'],
    'Russia': ['Moscow', 'Saint Petersburg'],
    'Rwanda': ['Kigali'],
    'Saudi Arabia': ['Riyadh'],
    'Scotland': ['Edinburgh'],
    'Senegal': ['Dakar'],
    'Serbia': ['Belgrade'],
    'Singapore': ['Singapore'],
    'Slovakia': ['Bratislava'],
    'Slovenia': ['Ljubljana'],
    'South Africa': ['Pretoria', 'Cape Town', 'Johannesburg'],
    'Spain': ['Madrid', 'Barcelona'],
    'Sri Lanka': ['Colombo'],
    'Sudan': ['Khartoum'],
    'Sweden': ['Stockholm'],
    'Switzerland': ['Bern', 'Zurich'],
    'Syria': ['Damascus'],
    'Taiwan': ['Taipei'],
    'Tanzania': ['Dodoma'],
    'Thailand': ['Bangkok'],
    'Tunisia': ['Tunis'],
    'Turkey': ['Ankara', 'Istanbul'],
    'UAE': ['Abu Dhabi', 'Dubai'],
    'Uganda': ['Kampala'],
    'Ukraine': ['Kyiv'],
    'United Kingdom': ['Bath', 'Belfast', 'Birmingham', 'Blackpool', 'Brighton', 'Bristol', 'Cambridge', 'Cornwall', 'Edinburgh', 'Glasgow', 'Liverpool', 'London', 'Manchester', 'Nottingham', 'Oxford', 'Scotland', 'Yorkshire'],
    'United States': ['Alabama', 'Alaska', 'Albany', 'Albuquerque', 'Arizona', 'Arkansas', 'Atlanta', 'Atlantic City', 'Austin', 'Baltimore', 'Berkeley', 'Beverly Hills', 'Boston', 'Bronx', 'Brooklyn', 'Buffalo', 'California', 'Cape Cod', 'Central Park', 'Charleston', 'Chicago', 'Chinatown', 'Cincinnati', 'Cleveland', 'Colorado', 'Connecticut', 'Coney Island', 'Dallas', 'Denver', 'Detroit', 'Florida', 'Georgia', 'Greenwich Village', 'Harlem', 'Hawaii', 'Hollywood', 'Honolulu', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Indianapolis', 'Kansas', 'Kansas City', 'Kentucky', 'Las Vegas', 'Lincoln', 'Long Beach', 'Long Island', 'Los Angeles', 'Louisiana', 'Maine', 'Malibu', 'Manhattan', 'Massachusetts', 'Memphis', 'Miami', 'Miami Beach', 'Michigan', 'Milwaukee', 'Minneapolis', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New England', 'New Hampshire', 'New Jersey', 'New Mexico', 'New Orleans', 'New York', 'Newark', 'Niagara Falls', 'Norfolk', 'North Carolina', 'North Pole', 'Northern California', 'Oakland', 'Ohio', 'Oklahoma', 'Omaha', 'Oregon', 'Palm Beach', 'Palm Springs', 'Pasadena', 'Pearl Harbor', 'Pennsylvania', 'Philadelphia', 'Phoenix', 'Pittsburgh', 'Portland', 'Reno', 'Rhode Island', 'Richmond', 'Rio Grande', 'Sacramento', 'Salem', 'Salt Lake City', 'San Antonio', 'San Diego', 'San Fernando Valley', 'San Francisco', 'Santa Barbara', 'Santa Fe', 'Santa Monica', 'Savannah', 'Seattle', 'South Carolina', 'Southern California', 'St. Louis', 'Staten Island', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington D.C.', 'West Virginia', 'Wisconsin', 'Wyoming'],
    'Uruguay': ['Montevideo'],
    'Vatican City': ['Vatican City'],
    'Venezuela': ['Caracas'],
    'Vietnam': ['Hanoi', 'Ho Chi Minh City'],
    'Wales': ['Cardiff'],
    'Yugoslavia': ['Belgrade'],
    }
    
    return {
        'character_metadata': character_metadata,
        'movie_metadata': movie_metadata,
        'plot_summaries': plot_summaries,
        'embeddings': embeddings,
        'combined_plot_summaries': combined_plot_summaries,
        'city_country_analysis': city_country_analysis,
        'cities_in_country' : cities_in_country
    }
    

client = OpenAI()
def get_embedding(text, model="text-embedding-ada-002"):
    """
    Get the embedding of a text using the OpenAI API.
    Can be used for similarity of movies, characters or for queries.
    """
    global client
    
    # We replace all line breaks with spaces
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    text = text.replace("\x0b", " ")
    text = text.replace("\x0c", " ")
    
    # We call the API and if it fails we wait 60 seconds.
    try:
        embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
        if embedding is None:
            print(f"Failed to process text: {text}. Error: embedding is None")
            return None
        return embedding
    except Exception as e:
        print(f"Failed to process text: {text}. Error: {str(e)}")
        # We wait 60 seconds because it means the API is rate limited
        time.sleep(60)
        return None
    
def extract_country(country_string):
    # Function to extract country name (first country name)
    if country_string:
        try:
            country_dict = json.loads(country_string)  # Convert string to dictionary using json
            if country_dict and isinstance(country_dict, dict):
                country_values = list(country_dict.values())
                if country_values:
                    return country_values[0]
        except json.JSONDecodeError:
            # Handle the case where the string is not a valid JSON
            pass
    return None

def get_color(ratio):
    "Determine the color based on the ratio for plots"
    if ratio < 1:
        return 'blue'
    elif 1 <= ratio < 1.5:
        return 'green'
    elif 1.5 <= ratio < 2:
        return 'yellow'
    elif 2 <= ratio < 2.5:
        return 'orange'
    else:
        return 'red'
    


def get_movie_names_from_ids(movie_ids, movie_metadata):
    """
    Get the movie names from the movie ids in order
    """
    movie_names = movie_metadata.loc[movie_metadata["Wikipedia movie ID"].isin(movie_ids), ['Wikipedia movie ID',"Movie name"]].values
    movie_names_dict = {movie_id: movie_name for movie_id, movie_name in movie_names}

    movie_names = []
    for movie_id in movie_ids:
        if movie_id not in movie_names_dict:
            # Sometimes plots are missing metadata, so we add "Unknown" as a placeholder
            movie_names.append("Unknown")
        else:
            movie_names.append(movie_names_dict[movie_id])
    
    return movie_names