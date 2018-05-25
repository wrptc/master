import os



def knp(filename):
    print('Start analysis:',filename)
    name = filename
    fname = name + '.txt'
    if len(name)<1:
        name = '28k'
        fname = '28k.txt'
    fhand = open(fname)
    doc = ''
    sentences = []
    knpresult = []
    num = 0
    for line in fhand:
        line = line.rstrip('\n')
        doc = doc + line
    sentences = doc.split('。')
    fhand.close()
    for sentence in sentences:
        print(num)
        num = num + 1
        tem = os.popen('echo '+sentence+' | juman | knp -simple').readlines()
        for details in tem:
            knpresult.append(details)
    fname = 'simple' + name + '.txt'
    fhand = open(fname,'w')
    for details in knpresult:
        fhand.write(details)
    fhand.close()

filenames = []
path = os.getcwd()
for root,dirs,files in os.walk(path):
    for filename in files:
        if filename.endswith('.txt'):
            filename = filename.strip('.txt')
            filenames.append(filename)
i=0
for filename in filenames:
    try:
        knp(filename)
        i+=1
    except:
        continue
