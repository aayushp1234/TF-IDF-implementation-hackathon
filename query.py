import math
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

def load_documents():
    documents = []
    with open("tf-idf/documents.txt", "r") as f:
        documents = f.readlines()
    # documents = [document.strip().split() for document in documents]
    return documents

def load_question_links():
    Qlinks = []
    with open("Leetcode-questionscrapper/Qindex.txt", "r") as f:
        Qlinks = f.readlines()
    return Qlinks

def load_inverted_index_values():
    inverted_index = {}
    with open("tf-idf/inverted-index-values.txt", "r") as f:
        inverted_index_terms = f.readlines()
    for row_num in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    return inverted_index

def load_vocab():
    vocab = {}
    with open("tf-idf/vocab-words.txt", "r") as f:
        vocab_words = f.readlines()
    with open("tf-idf/vocab-values.txt", "r") as f:
        vocab_values = f.readlines()
    for word, value in zip(vocab_words, vocab_values):
        vocab[word.rstrip()] = int(value.rstrip())
    return vocab

Qlinks = load_question_links()
vocab_idf_values = load_vocab()
document_headings = load_documents()
inverted_index = load_inverted_index_values()

# print(document[0])

def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for doc in inverted_index[term]:
            if doc not in tf_values:
                tf_values[doc] = 1
            else:
                tf_values[doc] += 1
    for doc in tf_values:
        try:
            tf_values[doc] /= len(document_headings[int(doc)])
        except(ZeroDivisionError, IndexError, ValueError) as e:
            print(e)
        # print (doc)
    return tf_values

def get_idf_values(term):
    return math.log(1 + len(document_headings) / (1 + vocab_idf_values[term]))

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    sorted_documents = []
    sorted_documents_indexes=[]

    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_values(term)
        
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            else:
                potential_documents[document] += tf_values_by_document[document] * idf_value
        
        for doc in potential_documents:
            potential_documents[doc] /= len(query_terms)
    
    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))
    
    if len(potential_documents) == 0:
        print("No matching question found. Please search with more relevant terms.")
    else:
        # print("Yes...found them")
        for document_index in potential_documents:
            if int(document_index) < len(document_headings):
                sorted_documents.append(Qlinks[int(document_index)])
                sorted_documents_indexes.append(document_headings[int(document_index)].title())
                # print("Document: ", Qlinks[int(document_index)], "Score: ", potential_documents[document_index], '\n')
    
    return [sorted_documents[:20:], sorted_documents_indexes[:20:]]

    # print(sorted_documents)
    # print(sorted_documents_indexes)

# query_string = input('Enter your input: ')
# query_terms = [term.lower() for term in query_string.strip().split()]
# print(query_terms)

# sorted_documents, sorted_document_indexes = calculate_sorted_order_of_documents(query_terms)
# for result1, result2 in zip(sorted_documents,sorted_document_indexes):
#     print(result1, result2)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query_string = request.form['query']
        titles=[]
        query_terms = [term.lower() for term in query_string.strip().split()]
        results,result_headings = calculate_sorted_order_of_documents(query_terms)
        for result in results:
            titles.append([Qlinks.index(result)])
        return render_template('index.html', results=results, titles=titles, result_headings=result_headings)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
