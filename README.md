# How does cinema view the world?

## Abstract
Our project focuses on uncovering biases in cinema, analyzing how films depict various cities and countries, often diverging from reality. We aim to critically examine these cinematic depictions, understanding how different eras and origins influence portrayals. This involves exploring the romanticization of cities like Paris versus the conflict-ridden portrayal of places like Afghanistan, assessing how these differ from real-world scenarios.

Our goal is to provide insights into cinema's role in shaping global perspectives, highlighting how film can reflect and distort cultural narratives and public opinion.

[Data Story](https://epfl-ada.github.io/ada-2023-project-tada/)

## Research Questions

- Are there stereotypes associated with cities?
    - Are particular genres (ex: action, thriller etc) associated with cities?
    - Are certain ideas and concepts (ex: love, drugs etc) overrepresented/underrepresented in cities?

- Does the country origin of a movie make a difference?
    - Are different countries depicted differently in movies with similar themes, and is this influenced by the origin country of the movie?
    - Are villains usually from certain regions, depending on the origin country of the movie?

- How are the antagonists depicted in movies?

- Are the ratings influenced by the location?

- Are stereotypes and movies influenced deeply by time?

- How accurately are human features such as names represented in movies?
    - Are there any relations to the country or city where the plot takes place? 

## Additional Datasets

We already have the CMU movie database (containing plot summaries for 42,306 movies). Additionally, we plan to use the IMDb as an additional source of information, containing 7 datasets. The `title.ratings.tsv.gz` dataset contains useful information regarding the weighted average of all the individual user ratings. We want to use ratings instead of box office in order to measure how good a movie is; for example, comparing the revenues of two movies, one in 1980 and one in 2010 might not be the best comparison due to inflation.

We will be able to easily handle the dataset size as it is not too large and we can use the API to query as much data as we need.

[IMDb ratings](https://developer.imdb.com/non-commercial-datasets/) \\
[Library](https://pypi.org/project/IMDbPY/)

## Methods

We will use a number of tools to answer our research questions, namely:
- **OpenAI ChatGPT API**: We will use the OpenAI ChatGPT API to help us in classifying movies as different countries and cities. This is a crucial part of our study and we are using OpenAI because they have the state of the art models for this task. In particular, we have used the GPT-3.5-Turbo model.

- **OpenAI Embeddings API**: To extract more nuanced meaning from the plot summaries we have used the OpenAI Embeddings API as we get a 1536 dimensional vector representing each summary which we can easily use for clustering.

- **Sentiment Analysis**: We will utilize NLP models to analyze the sentiment of plot summaries. We will use a pretrained model for this task. We are doing this in order to analyze if certain locations are associated with happy plots on average or not.

- **Statistical Analysis**: We will do different significance tests (t-test, etc.) and plots to highlight particular insights.

- **Clustering Analysis**: We will use clustering with embeddings in order to extract meaningful information such as preferred movie genres per country through the years.

- **Geospatial Analysis**: We will use Google map API to retrieve city and country coordinates for plotting maps.

- **Comparative Analysis**: We will  compare our results to real world statistics like the number of wars, the distribution of names and gender in order to find bias.

## Timeline

### First  (01 Dec - 07 Dec)
- Discussing P2 Feedback and any remarks for P3.
- Final adjustments with data processing.
- Analysis on genre distributions.
    - Explore the most popular genres (by cities/countries/continents).
    - Explore the time aspect of this.
- Analysis on historic events.
    - Explore wars.
    - Explore the time aspect of this.

### Second week (08 Dec - 14 Dec)
- Analysis on movie characters.
    - Antagonists and protagonists.
    - Name & gender representation.
- Assess how the country of production influences a film's perspective and narrative
    - Explore the bias some countries have for each other (ex. USA/Russia).
    - How historical events alter such views.
- Creating a coherent story from our many final analysis. 
- Checking the story is answering our research questions.
- Fine-tuning our plots and representations for our story.

### Third week (15 Dec - 20 Dec)
- Starting to transfer our story to the website.
- Create a nice website design to fit into our story.
- Make sure our visualizations fit correctly to our website and that the lecture is fluid.
- Publish the website with Github pages.
- Ensure the website works on all screen sizes.

### Last 2 days (21 and 22 Dec)
- Final checks for formatting and spelling.


## Organization

### Louis
- **Focus**: Foreign representation and gender analysis in movies.
  
### Ivan
- **Focus**: Distribution of movie genres.

### Stefan
- **Focus**: Depiction of historic events in films.

### David
- **Focus**: 
  - Data preprocessing.
  - Exploring how locations changed their view over time.
  - Development and maintenance of the project website.

### Tanguy
- **Focus**: 
  - Analysis of good vs. evil characters.
  - Most represented names by nationality.
  - Comparing findings with real-world data for validation.

### Team Collaboration
- **Role**: Collective writing of the research story.
- **Objective**: To provide comprehensive insights and uncover biases in cinema.

