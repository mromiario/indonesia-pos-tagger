#1301154311 - MUHAMMAD ROMI ARIO UTOMO - BASELINE

def read_file_init_table(fname): #Membaca dataset dan menghitung jumlah tag dan word
    tag_count = {}
    tag_count['<start>'] = 0
    word_tag = {}
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    counter = 1
    while (idx_line < len(content)) and (counter <= 1000): #membaca 1000 kalimat pertama
        while (not content[idx_line].startswith('</kalimat')):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                if content_part[1] in tag_count:
                    tag_count[content_part[1]] += 1
                else:
                    tag_count[content_part[1]] = 1
                    
                current_word_tag = content_part[0]+','+content_part[1]
                if current_word_tag in word_tag:
                    word_tag[current_word_tag] += 1
                else:    
                    word_tag[current_word_tag] = 1
            else:
                tag_count['<start>'] += 1

            idx_line = idx_line + 1

        idx_line = idx_line+1  
        counter+=1
    return tag_count, word_tag




def read_dataset(fname): #membaca data uji
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    counter = 1001
    while (idx_line < len(content)) and (counter<=1020): #membaca 20 kalimat setelahnya
        sent = []
        tag = []
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


####DATA TRAINING
tag_count, word_tag= read_file_init_table('Dataset.txt') #membaca data uji
#print(tag_count)
#print(word_tag)

#DATA TESTING

kalimat,tag_aktual = read_dataset('Dataset.txt') #membaca data latih
tag_uji=[] #array untuk menyimpan data uji

#Mencari tag dengan frekuensi yang paling sering muncul dari data uji yang diberikan
for i in range(len(kalimat)) :
    tag_uji_kalimat = []
    for j in range(len(kalimat[i])) :
        toMax = 0
        for key in tag_count.keys():
            word = kalimat[i][j]+','+key
            if word in word_tag :
                #print('Word :',word,'Value :',word_tag[word])
                if word_tag[word] > toMax : #membandingkan tag yang memiliki frekuensi paling besar
                    wordMax = word
                    toMax = word_tag[word] 
                    keyMax = key
        #print('Word:',wordMax,'Value max:',toMax, 'key max:', keyMax)
        tag_uji_kalimat.append(keyMax) #menyimpan tag dari satu kalimat dalam satu array
    tag_uji.append(tag_uji_kalimat) #array untuk menyimpan keseluruhan tag dari semua kalimat uji

#Menghitung akurasi
JumBenar = 0
TotalTag = 0
for i in range(len(kalimat)) :
    print('')
    str1 = ' '.join(kalimat[i])
    print('Kalimat:',str1)
    print('Tag sebenarnya :',tag_aktual[i])
    print('Tag uji :',tag_uji[i])
    for j in range(len(tag_aktual[i])) :
        if tag_aktual[i][j] == tag_uji[i][j] : 
            JumBenar += 1 #Menambah jumlah benar bila tag diprediksi benar
        else:
            print('KATA YANG SALAH :',kalimat[i][j])
            print('tag aktual :', tag_aktual[i][j])
            print('tag yang diuji salah :',tag_uji[i][j])
        #menampilkan kata dengan tag prediksi yang salah
        TotalTag +=1
print('')
print('Akurasi Baseline :',JumBenar/TotalTag*100)


