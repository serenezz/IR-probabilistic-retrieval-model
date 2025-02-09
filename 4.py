'''
CSC790 Assignment 4
Serene Zan

Instructions:
Open the terminal in the 'HW04 Zan' folder.
Please type 'python 4.py' to run the assignement.
'''

import os
import nltk as tk
import math



def read_file(file_path):
    '''
    Read strings from the document and store in a list.
    Parameters:
    1. file_path : str
        Path of the file.
    Returns:
    1. doc : list
        A list of strings read from the file.
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        doc = file.read().splitlines()

    return doc



def read_docs_from_folder(folder_path):
    '''
    Read documents from the folder and store in a list.
    Parameters:
    1. folder_path : str
        Path of the folder containing the docs.
    Returns:
    1. docs : dicitonary
        A dictionary: key - file number, value - doc strings read from the file.
    '''
    docs = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
                # Extract the number from file_1.txt
                number = int(file_name.split('.')[0].split('_')[-1])
                docs[number] = file.read().strip().replace('\n', ' ')

    return docs



def read_label(file_path):
    '''
    Read labels from the file and store in a dictionary.
    Parameters:
    1. file_path : str
        Path of the file containing the labels.
    Returns:
    1. labels : dicitonary
        A dictionary: key - file number, value - label of that file.
    '''
    labels = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        docs = file.read().splitlines()
        for doc in docs:
            file_id = int(doc.split(',')[0].split('_')[-1])
            label = int(doc.split(',')[1])
            # The numbering in the file is not the same
            labels[file_id] = label

    return labels



def tokenization(doc):
    '''
    Tokenize the string by calling the nltk method.
    Parameters:
    1. doc : string
        A text string.
    Returns:
    1. tokens : list
        A list of tokenzied terms.
    '''
    tokens = tk.word_tokenize(doc)
    return tokens



def removing(tokens, to_be_removed):
    '''
    Remove stop words/punctuation from the list of tokens.
    Parameters:
    1. tokens : list
        A list of tokenized terms.
    2. to_be_removed : list
        A list of stopwords/punctuation to be removed.
    Returns:
    1. processed_tokens : list
        A list of tokenized terms without stop words.
    '''
    processed_tokens = [word for word in tokens if not word in to_be_removed]
    return processed_tokens



def stemming(tokens):
    '''
    Stemming the tokens to match.
    Parameters:
    1. tokens : list
        A list of terms.
    Returns:
    1. stem_tokens : list
        A list of tokenized and stemmed terms without stopwords or punctuations.
    '''
    stem_tokens = [tk.stem.PorterStemmer().stem(word) for word in tokens]
    return stem_tokens



def preprocess_doc(doc, stop_words, punctuation):
    '''
    Preprocess the doc by calling functions for tokenization, stemming, and removing stopwords and punctuations.
    Parameters:
    1. doc : string
        A string from a document/query.
    2. stop_words : list
        A list of stop words.
    3. punctuation : list
        A list of punctuations.
    Returns:
    1. doc_processed : list
        A list containing the preprocessed terms of the document/query.
    '''
    # Tokenize
    doc = tokenization(doc)
    # Convert to lowercase
    doc = [word.lower() for word in doc]
    # Remove punctuation
    doc = removing(doc, punctuation)
    # Remove stop words
    doc = removing(doc, stop_words)
    # Stemming
    doc_processed = stemming(doc)

    return doc_processed



def compute_contingency(docs, labels, terms):
    '''
    Get the s, S - s, df values based on the docs and the query.
    Parameters:
    1. docs : dictionary
        A dictionary: key - file number, value - the tokens from the doc.
    2. labels : dictionary
        A dictionary: key - file number, value - label of that file.
    3. terms : list
        A list of preprocessed terms from the query.
    Returns:
    1. contingency : dictionary
        A dictionary: key - file number, value - dictionaries storing s, S-s, df values.
    2. terms_appearing : dictionary
        A dictionary: key - file number, value - terms that appear in both the doc and the query.
    '''
    terms_appearing = {}
    contingency = {}
    # Iteratre over the query terms
    for term in terms:
        df, s, S_s = 0, 0, 0
        # Iterate over the docs
        for file_id, doc in docs.items():
            # Present
            if term in doc:
                df += 1
                if file_id not in terms_appearing:
                    terms_appearing[file_id] = []
                # Add the terms that appear in both the doc and the query
                terms_appearing[file_id].append(term)
                # If relevant
                if labels[file_id] == 1:
                    s += 1
            # If absent
            else:
                # If relevant
                if labels[file_id] == 1:
                    S_s += 1
        df_pair = {'df': df}
        s_pair = {'s': s}
        S_s_pair = {'S-s': S_s}
        contingency[term] = {}
        contingency[term].update(df_pair)
        contingency[term].update(s_pair)
        contingency[term].update(S_s_pair)

    return contingency, terms_appearing



def compute_RSV(contingency, terms_appearing, N):
    '''
    Get the s, S - s, df values based on the docs and the query.
    Parameters:
    1. contingency : dictionary
        A dictionary: key - file number, value - dictionaries storing s, S-s, df values.
    2. terms_appearing : dictionary
        A dictionary: key - file number, value - terms that appear in both the doc and the query.
    3. N : int
        Total number of docs in the collection.
    Returns:
    1. RSVs : dictionary
        A dictionary: key - file number, value - RSV value of that doc.
    '''
    RSVs = {}
    # Iterate over the files that have terms from the query.
    for file_id, terms in terms_appearing.items():
        RSV = 0
        # Iterate over each term.
        for term in terms:
            s = contingency[term]['s']
            S_s = contingency[term]['S-s']
            df = contingency[term]['df']
            # Calculation
            RSV += math.log10(((s+0.5)/(S_s+0.5))/((df-s+0.5)/(N-df-S_s+0.5)))
        RSVs[file_id] = RSV
    
    # Sort the RSV and get top 10.
    RSVs = dict(sorted(RSVs.items(), key=lambda item: item[1], reverse=True)[:10])
    return RSVs



def display_info():
    '''
    Displays course and name.
    '''
    print('\n=================== CSC790-IR Homework 04 ===================')
    print('First Name: Serene')
    print('Last Name: Zan')
    print('============================================================')



def display_RSV(RSVs, label):
    '''
    Displays top 10 RSV and the label of that file.
    Parameters:
    1. RSVs : dictionary
        The dictionary containing RSV value for each file (key is file id).
    2. label : dictionary
        The dictionary containing label value for each file (key is file id).
    '''
    for file_id, RSV in RSVs.items():
        print(f'RSV file_{file_id} = {RSV}, {label[file_id]}')



def main():
    if __name__ == '__main__':

        # Read query
        query = read_file('query.txt')
        query = query[0]
        # Read all the docs from folder
        docs = read_docs_from_folder('documents')
        docs = dict(sorted(docs.items(), key=lambda x: int(x[0])))
        # Read the labels
        labels = read_label('file_label.txt')
        # Read stop words
        stop_words = read_file('stopwords.txt')
        # Read special char
        punctuation = read_file('chars.txt')

        # Preprocess query
        query_processed = preprocess_doc(query, stop_words, punctuation)

        # Preprocess docs
        docs_processed = {}
        for num, doc in docs.items():
            docs_processed[num] = preprocess_doc(doc, stop_words, punctuation)
        
        # Get contingency table (df, s, S-s)
        # Get the terms that appear in each doc
        contingency, term_appearing = compute_contingency(docs_processed, labels, query_processed)

        # Compute the RSV for each doc by summing up Ct
        N = len(docs_processed)
        RSVs = compute_RSV(contingency, term_appearing, N)
        
        # Display course info
        display_info()

        # Display top 10 RSV
        display_RSV(RSVs, labels)
        
     

main()