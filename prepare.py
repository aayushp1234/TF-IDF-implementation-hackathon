with open('Leetcode-questionscrapper/index.txt','r') as f:
    lines = f.readlines()
    # print(lines)

lines2=[]

for i in range(1, 2037):
    file_path = f'Leetcode-questionscrapper/Qdata/{i}/{i}.txt'
    with open(file_path, 'r') as f:
        for line in f:
            if ' Example' in line:
                break
        lines2.append(line.strip())

def preprocess(document_text):
    terms=[term.lower() for term in document_text.strip().split()[1:]]
    return terms

documents=[]
vocab={}
for index,line in enumerate(lines):
    # print(index,line)
    tokens=preprocess(line)
    documents.append(tokens)
    tokens=set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token]=1
        else:
            vocab[token]+=1

for index,line in enumerate(lines2):
    # print(index,line)
    tokens=preprocess(line)
    documents.append(tokens)
    tokens=set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token]=1
        else:
            vocab[token]+=1
# print("Number of documents: ",len(documents))
# print("Number of words: ",len(vocab))
# print("Sample Document: ",documents[1000])
# print("Sample Word Count: ",vocab['of'])
# print(vocab)
# print(documents)
vocab= dict(sorted(vocab.items(), key=lambda x: x[1], reverse=True))
with open("tf-idf/vocab-words.txt","w") as f:
    for key in vocab.keys():
        f.write(key +'\n')

with open("tf-idf/vocab-values.txt","w") as f:
    for key in vocab.keys():
        f.write(str(vocab[key])+'\n')

with open("tf-idf/documents.txt","w") as f:
    for document in documents:
        f.write(' '.join(document) +'\n')

inverted_index={}
for index,document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token]=[index]
        else:
            inverted_index[token].append(index)

with open("tf-idf/inverted-index-values.txt","w") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))

