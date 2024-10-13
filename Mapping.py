import re
import mysql.connector
import nltk
from fuzzywuzzy import fuzz

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# Tokenization and normalization functions
def tokenize_and_normalize(column_name):
    """Tokenizes and normalizes column names using NLTK."""
    tokens = word_tokenize(column_name)
    normalized_tokens = [token.lower() for token in tokens if token.isalnum()]
    return normalized_tokens

def get_synonyms(word):
    """Returns a set of synonyms for a given word using WordNet."""
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Function to compute similarity
def compute_similarity(col1, col2):
    """Computes similarity between two column names."""
    return fuzz.token_sort_ratio(col1, col2) / 100.0

def tokenize_and_normalize(column_name):
    """Tokenizes and normalizes column names using NLTK."""
    # Handle camelCase and snake_case
    tokens = re.findall(r'[A-Za-z][a-z]*|[A-Z][a-z]*', column_name)
    normalized_tokens = [token.lower() for token in tokens if token.isalnum()]
    return normalized_tokens

def is_abbreviation(word, potential_full_word):
    """Checks if a word is an abbreviation of another word."""
    # Check if word is a potential abbreviation of full word
    if len(word) > 1 and potential_full_word.startswith(word):
        return True
    return False

# Synonym expansion for dynamic abbreviation expansion using WordNet
def expand_abbreviations_using_context(word, possible_synonyms):
    """Expands a word if it's a possible abbreviation using its synonyms from WordNet."""
    for synonym in possible_synonyms:
        if is_abbreviation(word, synonym):
            return synonym
    return word

# Fetch synonyms using WordNet and check for possible matches
def get_expanded_tokens(column_name):
    """Gets expanded tokens for a column by checking abbreviations and expanding them using synonyms."""
    tokens = tokenize_and_normalize(column_name)
    expanded_tokens = []
    for token in tokens:
        synonyms = get_synonyms(token)  # Get synonyms from WordNet
        expanded_token = expand_abbreviations_using_context(token, synonyms)
        expanded_tokens.append(expanded_token)
    return expanded_tokens

def map_columns(asset_columns, asset_types, market_columns, market_types):
    """Map columns from the market table to the asset table based on similarity and type compatibility."""
    mapping = {}
    for market_col, market_type in zip(market_columns, market_types):
        market_tokens = get_expanded_tokens(market_col)  # Get expanded tokens for market columns
        for asset_col, asset_type in zip(asset_columns, asset_types):
            asset_tokens = get_expanded_tokens(asset_col)  # Get expanded tokens for asset columns
            
            # Check for type compatibility
            if market_type != asset_type:
                continue
            
            # Compute similarity score
            similarity = compute_similarity(' '.join(market_tokens), ' '.join(asset_tokens))
            
            # Filter out irrelevant mappings based on similarity threshold
            # print(str(market_tokens)+" "+str(asset_tokens)+" "+str(similarity))

            if similarity >= 0.4:  # Adjust the threshold as needed
                mapping[market_col] = asset_col
    
    return mapping


# def map_columns(asset_columns, asset_types, market_columns, market_types):
#     """Map columns from the market table to the asset table based on similarity and type compatibility."""
#     mapping = {}
#     for market_col, market_type in zip(market_columns, market_types):
#         market_tokens = tokenize_and_normalize(market_col)
#         for asset_col, asset_type in zip(asset_columns, asset_types):
#             asset_tokens = tokenize_and_normalize(asset_col)
            
#             # Check for type compatibility
#             if market_type != asset_type:
#                 continue
            
#             # Compute similarity score
#             similarity = compute_similarity(market_col, asset_col)
            
#             # Filter out irrelevant mappings based on similarity threshold
#             if similarity > 0.55:  # Adjust the threshold as needed
#                 mapping[market_col] = asset_col
    
#     return mapping

# Function to get all table names from the database
def get_table_names(cursor):
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]

# Function to get table information from the database
def get_table_info(cursor, table_name):
    cursor.execute(f"DESCRIBE {table_name}")
    return cursor.fetchall()

# Connect to the MySQL database
def connect_to_database(database_name):
    connection = mysql.connector.connect(
        host='127.0.0.1',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='@Aditya171',  # Replace with your MySQL password
        database=database_name
    )
    cursor = connection.cursor()
    return connection, cursor

def fetch_table_info(database_name):
    """Fetch and return table schema information as a dictionary."""
    connection, cursor = connect_to_database(database_name)
    table_info = {}
    
    # Fetch table names
    table_names = get_table_names(cursor)
    
    # Loop through the tables and get column information
    for table in table_names:
        columns = get_table_info(cursor, table)
        column_names = [column[0] for column in columns]  # Column names
        column_types = [column[1] for column in columns]   # Column types
        table_info[table] = (column_names, column_types)
    
    cursor.close()
    connection.close()
    
    return table_info

# Fetch table information for both databases
portfolio_info = fetch_table_info("PORTFOLIOS")
market_info = fetch_table_info("Market")

# Print fetched table information (Optional)
print("Portfolio Info:", portfolio_info)
print("Market Info:", market_info)

for market_table, (market_columns, market_types) in market_info.items():
    for portfolio_table, (portfolio_columns, portfolio_types) in portfolio_info.items():
        print(f"Mapping between {market_table} (Market) and {portfolio_table} (PORTFOLIOS):")
        mapping_result = map_columns(portfolio_columns, portfolio_types, market_columns, market_types)
        
        # Print the mapping result
        for market_col, portfolio_col in mapping_result.items():
            print(f"{market_col} -> {portfolio_col}")
        print("\n")