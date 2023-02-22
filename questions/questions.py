import nltk
import sys
import os
import string
import math
from time import sleep
#nltk.download('stopwords')
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    directories = os.listdir(directory)
    for dir in directories:
        file_path = os.path.join(directory, dir)
        with open(file_path, "r") as f:
            file_contents = f.read()
        files[dir] = file_contents
        #print(files[dir])

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    bag = nltk.word_tokenize(document)
    modified_bag = []
    for word in bag:
        word = word.lower()
        if word not in string.punctuation:
            if word not in nltk.corpus.stopwords.words("english"):
                modified_bag.append(word)
    return modified_bag


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = dict()
    for document in documents.values(): #each document is a list of words
        for word in document: #iterating through each words
            word_occurences = 0
            for document in documents.values(): #check to see if it's in another document
                if word in document: 
                    word_occurences += 1 #increment how many times that word shows up
            idf = math.log(len(documents.keys())/float(word_occurences))
            #print(idf)
            words[word] = idf
    return words
    
    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks = []
    for file in files:
        sum = 0
        for word in query:
            tf = 0
            for item in files[file]:
                if word == item:
                    tf += 1
            try:
                tfidf = tf * idfs[word]
            except:
                tfidf = 0
            sum += tfidf
        ranks.append({file: sum})
    #print(ranks)

    tops = sorted(ranks, key=lambda x: list(x.values())[0], reverse=True)
    tops = tops[0:n]
    returnlist = []
    for item in tops:
        returnlist.append(list(item.keys())[0])
    return returnlist
        

            
    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = []
    for sentence in sentences:
        sum = 0
        for word in query:
            tf = 0
            for item in sentences[sentence]:
                if word == item:
                    tf += 1
            try:
                tfidf = tf * idfs[word]
            except:
                tfidf = 0
            sum += tfidf
        ranks.append({sentence: sum})
    #print(ranks)

    tops = sorted(ranks, key=lambda x: list(x.values())[0], reverse=True)
    tops = tops[0:n]
    print("tops:")
    sleep(1)
    #print(tops)
    
    returnlist = []
    for item in tops:
        returnlist.append(list(item.keys())[0])
    
    return returnlist
    raise NotImplementedError


if __name__ == "__main__":
    main()
