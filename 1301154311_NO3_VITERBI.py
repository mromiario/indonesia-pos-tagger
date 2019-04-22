#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 06:06:55 2018

@author: mromiario
"""
import operator #library untuk mengambil value tertinggi dictionary
#Dibuat oleh Ibu Ade Romadhony
#Dikembangkan/dilengkapi oleh Muhammad Romi Ario Utomo - 1301154311

def read_file_init_table(fname): #membaca 1000 data untuk data training
    tag_count = {}
    tag_count['<start>'] = 0
    word_tag = {}
    tag_trans = {}
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    is_first_word = 0
    counter = 1
    while (idx_line < len(content)) and (counter <= 1000):#membatasi data yang diolah, 1000 data pertama
        prev_tag = '<start>'
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
                    
                if is_first_word == 1:
                    current_tag_trans = '<start>,'+content_part[1]
                    is_first_word = 0
                else:
                    current_tag_trans = prev_tag+','+content_part[1]
                    
                if current_tag_trans in tag_trans:
                    tag_trans[current_tag_trans] += 1
                else:
                    tag_trans[current_tag_trans] = 1                    
                prev_tag = content_part[1]   
                
            else:
                tag_count['<start>'] += 1
                is_first_word = 1
            idx_line = idx_line + 1

        idx_line = idx_line+1  
        counter+=1
    return tag_count, word_tag, tag_trans



def create_trans_prob_table(tag_trans, tag_count): #Membuat matriks transisi
    #print(tag_trans)
    trans_prob = {}
    for tag1 in tag_count.keys():
        for tag2 in tag_count.keys():
            #print('tag1 = ')
            #print(tag1)
            trans_idx = tag1+','+tag2
            #print('trans_idx = ')
            #print(trans_idx)
            if trans_idx in tag_trans:
                #print(trans_idx)
                trans_prob[trans_idx] = tag_trans[trans_idx]/tag_count[tag1]
    return trans_prob


def create_emission_prob_table(word_tag, tag_count): #Membuat matriks emisi
    emission_prob = {}
    for word_tag_entry in word_tag.keys():
        word_tag_split = word_tag_entry.split(',')
        if word_tag_entry[0] == ',' :
            current_word = word_tag_entry[0]
            current_tag = word_tag_entry[2:]
        else :
            current_word = word_tag_split[0]
            current_tag = word_tag_split[-1] #mengambil tag, karena posisi tag di array terakhir
        emission_key = current_word+','+current_tag
        emission_prob[emission_key] = word_tag[word_tag_entry]/tag_count[current_tag]    
    return emission_prob



def viterbi(trans_prob, emission_prob, tag_count, sentence): #Membuat matriks vitervi
    #initialization
    viterbi_mat = {}
    tag_sequence = []
    prev_word = ''
  
    sentence_words = sentence.split()
    for i in range(len(sentence_words)):
        viterbi_mat[sentence_words[i]] = {} #pendefinisian dictionary di dalam dictionary
        for tag in tag_count.keys() :
            viterbi_mat[sentence_words[i]][tag]=0 #membuat dictionary word yang isi dari setiap word adalah dictionary tag
        
    for i in range(len(sentence_words)):
        if i==0 :
            prev_key = str('<start>') #kondisi kata yang ada di awal kalimat
            max_value = 1 #Nilai maksimal dari tag start

        
        for key in tag_count.keys() :
            trans = str(prev_key+','+key)
            emis = str(sentence_words[i]+','+key)
            if (trans in trans_prob) and (emis in emission_prob):
                viterbi_mat[sentence_words[i]][key] = max_value*trans_prob[trans]*emission_prob[emis] #Mengalikan nilai maksimum sebelumnya dengan niai probabilitas trans dan emisi

        prev_word=sentence_words[i]
        prev_key = max(viterbi_mat[prev_word].items(), key=operator.itemgetter(1))[0] #backtracking mencari hasil perkalian yang paling maksimal
        if (viterbi_mat[prev_word][prev_key] != 0) :
            max_value = viterbi_mat[prev_word][prev_key]
            tag_sequence.append(prev_key) #menyimpan sekuens
        else :
            tag_sequence.append('NN') #kondisi apabila kata tidak ada di kamus latih, tagnya diassign NN
    return viterbi_mat, tag_sequence

def read_dataset(fname): #Membaca dataset yang digunakan sebagai data uji
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    counter = 1001
    while (idx_line < len(content)) and (counter<=1020): #mengambil kalimat 1001 - 1020
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
tag_count, word_tag, tag_trans = read_file_init_table('Dataset.txt') #membaca dan mengolah data latih
#print(tag_count)
#print(word_tag)
trans_prob = create_trans_prob_table(tag_trans, tag_count) #membuat matriks transisi
#print(trans_prob)
emission_prob = create_emission_prob_table(word_tag, tag_count) #membuat matriks emisi
#print(emission_prob)

#DATA TESTING

kalimat,tag_aktual = read_dataset('Dataset.txt') #membaca data uji
JumBenar = 0
TotalTag = 0
for i in range(len(kalimat)) :
    print('')
    str1 = ' '.join(kalimat[i])
    print('Kalimat:',str1)
    matriks_viterbi, tag_uji = viterbi(trans_prob, emission_prob, tag_count, str1)
    print('Tag sebenarnya :',tag_aktual[i])
    print('Tag uji :',tag_uji)
    for j in range(len(tag_aktual[i])) :
        if tag_aktual[i][j] == tag_uji[j] :
            JumBenar += 1 #menghitung jumlah tag yang diprediksi benar
        else:
            print('KATA YANG SALAH :',kalimat[i][j])
            print('tag aktual :', tag_aktual[i][j])
            print('tag yang diuji salah :',tag_uji[j])
        TotalTag +=1 #menghitung jumlah tag keseluruhan
print('')
print('Akurasi Viterbi :',JumBenar/TotalTag*100) #menghitung akurasi

