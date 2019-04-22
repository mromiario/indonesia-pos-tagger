# Contoh POSTagger sederhana dengan pendekatan statistika (metode decision tree)
# Ade Romadhony - Fakultas Informatika Universitas Telkom
# sumber: https://nlpforhackers.io/training-pos-tagger/

#Dikembangkan oleh Muhammad Romi Ario Utomo - 1301154311

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline


def read_dataset(fname):
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    counter = 1
    while (idx_line < len(content)) and (counter <= 1020): #Load data agar terbaca 1020 Data
        sent = []
        tag = []
        print('idx_line =')
        print(idx_line)
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        sentences.append(sent)
        tags.append(tag)
        idx_line = idx_line+2  
        counter+=1
    return sentences, tags

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],#3 karakter diawal
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],#3 karakter di akhir
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    }


 
def transform_to_dataset(sentences, tags):
    X, y = [], []
 
    for sentence_idx in range(len(sentences)):
        for index in range(len(sentences[sentence_idx])):
            X.append(features(sentences[sentence_idx], index))
            y.append(tags[sentence_idx][index])
 
    return X, y
 
def pos_tag(sentence,clf):
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    #return zip(sentence, tags)
    return tags

def classifier(klf)     :
    clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', klf )
])
    clf.fit(X, y) 
    print('Training completed')

    return clf
 
sentences,tags = read_dataset('Dataset.txt')
# Split the dataset for training and testing
training_sentences = sentences[:1000] #Menjadi 1000 data pertama menjadi data latih
test_sentences = sentences[1000:] #Menjadikan data selanjutnya menjadi data uji
training_tags = tags[:1000] #Menyimpan tag data latih
test_tags = tags[1000:] #Menyimpan tag data uji
print('Load data')

X, y = transform_to_dataset(training_sentences, training_tags)
X_test, y_test = transform_to_dataset(test_sentences, test_tags)
print('Transform to dataset')
clf_ = classifier(tree.DecisionTreeClassifier(criterion='entropy')) #Memanggil classifier ID3

for i in range(len(test_sentences)) :
    print('================================')
    print('Kalimat :',test_sentences[i])
    print('')
    predict_tag = pos_tag(test_sentences[i],clf_)
    print('Tag prediksi :',predict_tag)
    print('')
    print('Tag sebenarnya :',test_tags[i])
    print('')
    for j in range(len(predict_tag)) :
        if(test_tags[i][j]!=predict_tag[j]):
            print('KATA SALAH :',test_sentences[i][j])
            print('Tag sebenarnya :',test_tags[i][j])
            print('Tag prediksi :',predict_tag[j])
            
        

print("Accuracy ID3:")
print(clf_.score(X_test, y_test)*100,'%')


### Test model yang sudah dilatih dengan kalimat masukan bebas
#from nltk import word_tokenize 
#print(pos_tag(word_tokenize('kera untuk amankan pesta olahrafa'),clf_))
# 
