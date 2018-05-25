import re
import os

def readfiles():
    filenames = []
    for root,dirs,files in os.walk(os.getcwd()):
        for filename in files:
            if filename.endswith('.txt'):
                if filename[:-4].isdigit():
                    filenames.append(filename[:-4])
    return filenames


def findevent(name):
    events = []
    print('Reading:',name)
    fname = name + '.txt'
    fhand = open(fname,'r')
    pattern = re.compile('<格解析結果:.+>')
    p=['ガ','ヲ','ニ','ト','デ','カラ','ヨリ','マデ','ヘ','時間']
    for line in fhand.readlines():
        if '格解析結果:' not in line:continue
        tem = pattern.findall(line)[0].split(':')
        if '動' not in tem[2]:continue
        event = ''
        verb = tem[1].split('/')[0]
        details = tem[3]
        detail = details.split(';')
        caseinfo = ''
        mode = 0
        for item in detail:
            if '-' in item:continue
            for case in p:
                if case in item:
                    mode = 1
                    noun = item.split('/')[2]
                    caseinfo += case +':'+noun+name+'/'
        if mode ==1:
            event += verb+'/'+caseinfo
            events.append(event)
    return events

def find_cliques(G):
    if len(G) == 0:
        return

    adj = {u: {v for v in G[u] if v != u} for u in G}
    Q = [None]

    subg = set(G)
    cand = set(G)
    u = max(subg, key=lambda u: len(cand & adj[u]))
    ext_u = cand - adj[u]
    stack = []

    try:
        while True:
            if ext_u:
                q = ext_u.pop()
                cand.remove(q)
                Q[-1] = q
                adj_q = adj[q]
                subg_q = subg & adj_q
                if not subg_q:
                    yield Q[:]
                else:
                    cand_q = cand & adj_q
                    if cand_q:
                        stack.append((subg, cand, ext_u))
                        Q.append(None)
                        subg = subg_q
                        cand = cand_q
                        u = max(subg, key=lambda u: len(cand & adj[u]))
                        ext_u = cand - adj[u]
            else:
                Q.pop()
                subg, cand, ext_u = stack.pop()
    except IndexError:
        pass

def mkpairs(filename):
    fhand=open(filename)
    for line in fhand.readlines():
        tem = line.split('/')
        verb = tem[0]
        cases = tem[1:]
        for item in cases:
            if ':' not in item:continue
            info = item.split(':')
            case = info[0]
            vc = verb+'/'+case
            noun = info[1]
            pair = [vc,noun]
            G.add_node(pair[0],weight=0)
            G.add_node(pair[1],weight=1)
            G.add_edge(pair[0],pair[1])
            if pair[0] not in vc_set:
                vc_set.append(pair[0])
            if pair[1] not in noun_set:
                noun_set.append(pair[1])
    fhand.close()


if __name__=='__main__':
    filenames = readfiles()
    fhand = open('events.txt','w')
    for filename in filenames:
        for items in findevent(filename):
            fhand.write(items+'\n')
    fhand.close()
    '''
    G = nx.Graph()
    vc_set = []
    noun_set = []
    mkpairs('events.txt')
    for vc_a in vc_set:
        for vc_b in vc_set:
            if vc_a == vc_b:continue
            G.add_edge(vc_a,vc_b)
    vclen = len(vc_set)
    for n_a in noun_set:
        for n_b in noun_set:
            if n_a == n_b:continue
            G.add_edge(n_a,n_b)
    nlen = len(noun_set)
    cliques = nx.find_cliques(G)
    for item in cliques:
        if len(item)<3:continue
        if len(item)==vclen:continue
        if len(item)==nlen:continue
        print(item)
    '''
