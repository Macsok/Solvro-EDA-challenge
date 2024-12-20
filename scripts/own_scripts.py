import pandas as pd
from typing import Tuple
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def unpack_data_json(df_column: pd.DataFrame) -> pd.DataFrame:
    """Takes pandas DataFrame column as an input. 
    Iterates rows and upacks them. Returns new dataframe as a result"""
    result = pd.DataFrame([])

    for index in range(df_column.shape[0]):
        #concats result DataFrame with json data in current row
        result = pd.concat([result, pd.json_normalize(df_column[index])])

    return result


def unpack_and_assign_id(
        df_column: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Takes pandas DataFrame column as an input. 
    Iterates rows and upacks them. 
    Returns new dataframe and list of lists of indexes as a result"""
    result = pd.DataFrame([])
    indexes = list()

    for index in range(df_column.shape[0]):
        #extract and append list of indexes
        ingr = pd.json_normalize(df_column[index])
        indexes.append(ingr['id'].to_list())

        #concats result DataFrame with json data in current row
        result = pd.concat([result, ingr])

    return result, indexes


def analyze_ingredients(
        data: pd.DataFrame,
        ingredients: pd.DataFrame) -> dict:
    """Takes DataFrame as an input and outputs dictionary of all ingredients 
    (records from separate DataFrame) found in the 'ingredientsID' tab where 
    a key is apperance of each element."""
    #set new indexing in list
    data = data.reset_index()
    #initialize new dictionary to count every element apperance
    counts = {}

    for index in range(data.shape[0]):
        ingr_list = data['ingredientsID'][index]
        #counting every ingredient apperance
        for ingredient in ingr_list:
            try:
                counts[ingredients.iloc[ingredient]['name']] += 1
            except:
                counts[ingredients.iloc[ingredient]['name']] = 1
    return counts


def dataset_preprocessing(
        df: pd.DataFrame, 
        drop_times: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocesses provided dataset (specified for cocktail_dataset). 
    Returns tuple of pd.DataFrame, [df, ingredniets_column]. 
    Set drop_times to False to get timestamps"""

    # extracting ingredients column
    ingredients, df['ingredientsID'] = unpack_and_assign_id(df['ingredients'])

    # droping columns
    df = df.drop(columns = ['imageUrl', 'ingredients', 'tags', 'alcoholic'])
    ingredients = ingredients.drop(columns = ['imageUrl', 'measure'])

    if drop_times:
        df = df.drop(columns = ['createdAt', 'updatedAt'])
        ingredients = ingredients.drop(columns = ['createdAt', 'updatedAt'])
        return df, ingredients

    # correcting data types
    for header in ['percentage']:
        ingredients[header] = ingredients[header].apply(lambda a: 0 if pd.isna(a) else a)

    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df['updatedAt'] = pd.to_datetime(df['updatedAt'])

    ingredients['createdAt'] = pd.to_datetime(ingredients['createdAt'])
    ingredients['updatedAt'] = pd.to_datetime(ingredients['updatedAt'])

    return df, ingredients


def ingredients_to_names(
        ingredients: pd.DataFrame, 
        ingredients_list: pd.DataFrame) -> pd.DataFrame:
    """Matches each ingredients list with names, returns a column of names in lists. 
    Set to_list option to True to get results in list."""
    # TODO: optimalization
    # intitailization, and copying the data column
    column_copy = ingredients_list.copy()

    for index in range(ingredients_list.shape[0]):
        name_list = list()
        end = len(ingredients_list[index])

        for i in range(end):
            # find and append names to list
            current = ingredients.loc[ingredients['id'] == ingredients_list[index][i]].drop_duplicates()
            current = current['name'].to_list()[0]
            name_list.append(current)

        column_copy[index] = ', '.join(name_list)
    
    return column_copy


def recommend_cocktails(
        cocktail_name: str, 
        df: pd.DataFrame):
    """Takes actual cocktail name and DataFrame (with ingredients list column), 
    counts similarity between cocktails and returns 3 most matching cocktails (from most to least similar)."""

    # vectorizing ingredients
    vectorizer = CountVectorizer()
    ingredient_matrix = vectorizer.fit_transform(df['ingredients'])

    # cosine similarity matrix
    similarity_matrix = cosine_similarity(ingredient_matrix)

    indices = pd.Series(df.index, index=df['name']).drop_duplicates()
    idx = indices[cocktail_name]
    
    # sorting according to similarity
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # choose 3 most matching ones
    sim_scores = sim_scores[1:4]
    cocktail_indices = [i[0] for i in sim_scores]
    
    return df['name'].iloc[cocktail_indices].to_list()


def print_similar_cocktails(
        df: pd.DataFrame, 
        similar_to: str) -> None:
    """Prints most similar cocktails to provided one."""
    # set display width to maximum
    pd.set_option('display.max_colwidth', None)
    print('Your cocktail:')
    display(df.loc[ df['name'] == similar_to])
    print('Suggested coctails (most similar at the top):')
    res = pd.DataFrame([])
    for one in recommend_cocktails(similar_to, df): res = res.append(df.loc[ df['name'] == one], ignore_index=True)
    display(res)


def clusterization(
        df: pd.DataFrame, 
        clusters: int) -> pd.DataFrame:
    """Clusters provided DataFrame by similarity of ingredients used."""
    # vectoriznig and clustering using scikit-learn
    vectorizer = CountVectorizer()
    ingredient_matrix = vectorizer.fit_transform(df['ingredients'])
    kmeans = KMeans(n_clusters=clusters)
    
    return pd.DataFrame(kmeans.fit_predict(ingredient_matrix))


def plot_cocktail_clusters(
        df: pd.DataFrame, 
        n_clusters: int = 3, 
        print_labels: bool = True) -> plt.Axes:
    """Plots every cocktail of each cluster in diffrent colour (5 different)."""
    # Convert 'ingredients' to a matrix of token counts
    vectorizer = CountVectorizer()
    ingredient_matrix = vectorizer.fit_transform(df['ingredients'])

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters)
    df['cluster'] = kmeans.fit_predict(ingredient_matrix)

    # PCA (Principal Component Analysis) transformation for visualization
    pca = PCA(n_components=2)
    ingredient_pca = pca.fit_transform(ingredient_matrix.toarray())

    # Convert to DataFrame
    pca_df = pd.DataFrame(ingredient_pca, columns=['PC1', 'PC2'])
    pca_df['cluster'] = df['cluster']
    pca_df['name'] = df['name']

    # Plotting the clusters
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = ['blue', 'green', 'red', 'purple', 'pink']  # Adjust for more clusters
    markers = ['o', 's', 'D', '^', 's']  # Adjust for more clusters

    for cluster in pca_df['cluster'].unique():
        subset = pca_df[pca_df['cluster'] == cluster]
        ax.scatter(subset['PC1'], subset['PC2'], c=colors[cluster % 5], marker=markers[cluster % 5], label=f'Cluster {cluster % 5}')
        if print_labels:
            for i in range(subset.shape[0]):
                ax.text(subset['PC1'].iloc[i], subset['PC2'].iloc[i], subset['name'].iloc[i], fontsize=9)

    ax.set_title('Cocktail Clusters')
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.legend()
    ax.grid(True)

    return ax