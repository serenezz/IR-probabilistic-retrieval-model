# CSC790 - Probabilistic Information Retrieval

### Overview
This assignment implements an information retrieval system that processes and ranks documents based on a query using the RSV (Relevance Score Value) model. The system tokenizes, preprocesses, and computes document scores to retrieve the most relevant results.

### Tasks
Download the folder HW04 from Brightspace. The folder contains the following:
1. **documents/** - Contains the text files.
2. **file_label.txt** - Contains file relevance labeling in the format: `[file name, rel]`, where `rel ∈ {0,1}`.
3. **query.txt** - A file containing the query.

### File Structure
- `4.py` - Main script that runs the assignment
- `query.txt` - Contains the search query
- `documents/` - Folder containing text documents to be processed
- `file_label.txt` - File containing document relevance labels
- `stopwords.txt` - List of stopwords to be removed during preprocessing
- `chars.txt` - List of punctuation characters to be removed during preprocessing

### Functionality
The script performs the following steps:
1. Reads the input query from `query.txt`.
2. Loads and preprocesses documents from the `documents/` directory.
3. Tokenizes, removes stop words, stems, and normalizes terms.
4. Computes the contingency table for document-query term matches.
5. Computes the RSV scores for documents.
6. Displays the top 10 ranked documents based on RSV scores.
