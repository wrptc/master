import os
import networkx as nx
import time

def getfilenames():
    filenames = []
    path = os.getcwd()
    for root,dirs,files in os.walk(path):
        for filename in files:
            if filename.endswith('.txt'):
                filename = filename[:-4]
                if filename.isdigit():
                    filenames.append(filename)
    return filenames


def keygraph(filename):
    M_1 = 3*int(MM)
    M_2 = int(MM)
    name = filename
    fname = name + '.txt'
    fhand = open(fname)
    print('Reading:%s' %fname)
    word_set = {} #{(apple,1):1}
    sentence_num = 0
    for line in fhand:
        if line.startswith('#'):
            sentence_num += 1
        knpresult = line.split()
        if '普通名詞' in knpresult:
            for keys in knpresult:
                if not keys.startswith('"代表表記:'):continue
                word = keys.split(':')[1]
                if word.endswith('v'):continue
                word = word.split('/')[0]
                word_set[(word,sentence_num)] = word_set.get((word,sentence_num),0)+1
    fhand.close()
    words = {} #words:{apple:times}
    for word,times in word_set.items():
        words[word[0]] = words.get(word[0],0) + times
    tem = []
    for word,times in word_set.items():
        tem.append((times,word))
    tem.sort(reverse = True)
    m_1 = min(M_1,len(words))
    tem = tem[:m_1]
    HighFreq = []
    for (times,word) in tem:
        HighFreq.append(word)
    co_occurrence = {}
    co_tem = {}
    for word1,times1 in word_set.items():
        for word2,times2 in word_set.items():
            if word1[1] != word2[1]:continue
            if word1[0] == word2[0]:continue
            co = times1 * times2
            co_occurrence[(word1[0],word2[0])] = co_occurrence.get((word1[0],word2[0]),0)+co
    for pairs,co in co_occurrence.items():
        if (pairs[1],pairs[0]) in co_tem:continue
        co_tem[pairs[0],pairs[1]] = co
    co_set = {}
    for word1 in HighFreq:
        for word2 in HighFreq:
            if (word1,word2) in co_tem:
                co_set[(word1,word2)] = co_tem[(word1,word2)]
    tem = []
    for pairs,co in co_set.items():
        tem.append((co,pairs))
    tem.sort(reverse = True)
    tem = tem[:m_1-1]
    links = []
    for (co,pairs) in tem:
        links.append(pairs)
    foundations = {}
    for word in HighFreq:
        if word not in foundations:
            foundations[word] = []
    for(word1,word2) in links:
        foundations[word1].append(word2)
        foundations[word2].append(word1)
    G = nx.Graph(foundations)
    graphs = list(nx.connected_component_subgraphs(G))
    g_s_set = {}
    for word,times in word_set.items():
        for i in range(len(graphs)):
            if word[0] not in graphs[i].nodes():continue
            g_s_set[(i,word[1])] = g_s_set.get((i,word[1]),0) + times
    based_set = {}
    for i in range(len(graphs)):
        for word,times in word_set.items():
            if word[0] in graphs[i].nodes():
                g_minus_w = g_s_set[(i,word[1])] - times
            else:
                g_minus_w = times
            based = times* g_minus_w
            based_set[(word[0],i)] = based_set.get((word[0],i),0) + based
    neighbors_set = {}
    for i in range(len(graphs)):
        for word,times in word_set.items():
            if word[0] in graphs[i].nodes():
                g_minus_w = g_s_set[(i,word[1])] = times
            else:
                g_minus_w = times
                neighbors_set[i] = neighbors_set.get(i,0) + g_minus_w
    key_set = {}
    tem_set = {}
    for word in word_set:
        for i in range(len(graphs)):
            based = based_set[(word[0],i)]
            neighbors = neighbors_set[i]
            tem = 1-based/neighbors
            tem_set[word[0]] = tem_set.get(word[0],1) * tem
        key_set[word[0]] = 1-tem
    m_2 = min(M_2,len(words))
    tem = []
    for word,key in key_set.items():
        tem.append((key,word))
    tem.sort(reverse = True)
    tem = tem[:m_2]
    key = []
    for i,j in tem:
        key.append((str(j)+name,i))
    return key

if __name__ == '__main__':
    filenames = getfilenames()
    keyfhand = open('keyword.txt','w')
    t0 = time.time()
    MM = input("n parameter for Top-n keywords?\n")
    for filename in filenames:
        key = keygraph(filename)
        for i,j in key:
            line = str(i) + '/' + str(j) + '\n'
            keyfhand.write(line)
    t1 = time.time()
    print(t1-t0)
