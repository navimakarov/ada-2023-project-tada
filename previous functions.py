



Functions that worked 


#### This function worked but : There are some mistakes such as 30637679 : 'I Want to Go Home' : loc = 30513 : 
# which takes place in paris and is made by a french production as movie_metadata['Movie countries (Freebase ID:name tuples)'][30513] outputs : '{}'

# Filter movie IDs based on the country in movie_metadata
filtered_city_lists = {}

for city, movie_ids in city_lists.items():
    filtered_movie_ids = []

    for movie_id in movie_ids:
        
        matching_movies = movie_metadata[movie_metadata['Wikipedia movie ID'] == movie_id]
        if not matching_movies.empty:
            
            movie_country = matching_movies.iloc[0]['Country']
            city_country = next((country for country, cities in cities_in_country.items() if city in cities), None)
            if movie_country != city_country:
                filtered_movie_ids.append(movie_id)
    filtered_city_lists[city] = filtered_movie_ids

# Print the filtered lists for each city
for city, movie_ids in filtered_city_lists.items():
    print(f"{city}: {movie_ids}")






# Create a dictionary to regroup movie IDs by city and country
regrouped_by_city_and_country = {}

for city, movie_ids in foreign_movies.items():
    for movie_id in movie_ids:
        matching_movies = movie_metadata[movie_metadata['Wikipedia movie ID'] == movie_id]
        if not matching_movies.empty:
            movie_country = matching_movies.iloc[0]['Country']
            if movie_country is not None:
                if city not in regrouped_by_city_and_country:
                    regrouped_by_city_and_country[city] = {}
                if movie_country not in regrouped_by_city_and_country[city]:
                    regrouped_by_city_and_country[city][movie_country] = []
                regrouped_by_city_and_country[city][movie_country].append(movie_id)

""" # Now you can access the movie IDs grouped by city and country
# For example, to access movies in Paris from different countries:
paris_movies = regrouped_by_city_and_country.get('Paris', {})
for country, movie_ids in paris_movies.items():
    print(f"Movies in Paris from {country}: {movie_ids}")

# To access movies in Berlin from different countries:
berlin_movies = regrouped_by_city_and_country.get('Berlin', {})
for country, movie_ids in berlin_movies.items():
    print(f"Movies in Berlin from {country}: {movie_ids}")
 """



# Create a dictionary to store filtered movie IDs for each city
foreign_movies = {}

# Iterate over cities in cities_in_country
for country, cities in cities_in_country.items():
    for city in cities:
        filtered_movie_ids = []
        city_movies = city_lists.get(city, [])  # Get movies for the current city
        for movie_id in city_movies:
            matching_movies = movie_metadata[movie_metadata['Wikipedia movie ID'] == movie_id]
            if not matching_movies.empty:
                movie_country = matching_movies.iloc[0]['Country']
                if movie_country is not None and movie_country != country:
                    filtered_movie_ids.append(movie_id)
        foreign_movies[city] = filtered_movie_ids

# Print the filtered lists for each city
for city, movie_ids in foreign_movies.items():
    print(f"{city}: {movie_ids}")