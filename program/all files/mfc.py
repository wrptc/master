import networkx as nx
import time
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
        line = line.rstrip('\n')
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
            if noun in keys:
                G.add_node(pair[0],weight=0)
                G.add_node(pair[1],weight=1)
                G.add_edge(pair[0],pair[1])
                if pair[0] not in vc_set:
                    vc_set.append(pair[0])
                if pair[1] not in noun_set:
                    noun_set.append(pair[1])
    fhand.close()

if __name__ == '__main__':
    whand = open('result.txt','w')
    s = int(input("please input tau parameter:\n"))
    t0 = time.time()
    fhand = open('keyword.txt')
    keys = []
    for line in fhand:
        keys.append(line.split('/')[0])
    

    G = nx.Graph()
    vc_set = []
    noun_set = []
    print('Set graph...')
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
    print('Start finding cliques...')
    cliques = nx.find_cliques(G)
    num = 0
    rolesetlist = []
    dictionary = {}
    for clique in cliques:
        
        num+=1
        if len(clique)<3:continue
        if len(clique)==vclen:continue
        if len(clique)==nlen:continue
        
        v_c = []
        n_d = []
        for i in clique:
            if '/' in i:
                v_c.append(i)
            else:
                n_d.append(i)
            v_c.sort()
        if len(n_d)==1:continue
        print(clique)
        t = []
        for i in n_d:
            t.append(i.split('0')[-1])
        t = set(t)
        
        if len(t) < s:continue
        rolesetlist.append(set(v_c))
        dictionary_key = ''
        for name in v_c:
            dictionary_key +=name+' '
        dictionary[dictionary_key]=n_d
        #print(v_c,n_d)
    print('extand role set:...')
    extended = []
    for roleset1 in rolesetlist:
        mode = 0
        for roleset2 in rolesetlist:
            if roleset2>roleset1:
                mode = 1
                break
        if mode == 0:
            tem = list(roleset1)
            tem.sort()
            extended.append(tem)
    print('\n')
    print('############')
    for roleset in extended:
        tem = []
        for v_c in roleset:
            tem.append(v_c)
        dic_key = ''
        for name in tem:
            dic_key+=name+' '
        n_d = dictionary[dic_key]

        whand.write(str(roleset)+str(n_d)+'\n')
        print(roleset,n_d)
    t1 = time.time()
    print((t1-t0)/4)