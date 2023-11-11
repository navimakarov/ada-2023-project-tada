# We will download the dataset + the processed embeddings(obtained via the calculate-embeddings.ipynb notebook) from Google Drive
import gdown
import os

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
    
# Download the dataset(a folder)
id = '1AO6EznTNmZ0PtBEexL80P9neFcZhSZkT'
output = 'data/'
gdown.download_folder(id=id, quiet=False, output=output)