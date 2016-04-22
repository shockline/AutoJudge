import codecs


    

def read_file(f, d, label): 
    for line in f:
        line = line.strip()
        print line
        if len(line) == 0:
            continue
        line = line.split('\t')
        if len(line) < 2:
            continue
        d[(line[0].strip(), line[1].strip())] = label

def write_file(f, d, label):
    res = list()
    for k, v in d.items():
        if v == label:
            res.append(k)
    def compare(x, y):
        if x[0] == y[0]:
            if x[1] < y[1]:
                return -1
            elif x[1] == y[1]:
                return 0
            else:
                return 1
        else:
            if x[0] < y[0]:
                return -1
            elif x[0] == y[0]:
                return 0
            else:
                return 1
    res = sorted(res, cmp=compare)
    for k in res:
        f.write('%s\t%s\n' % k)

d = dict()

with codecs.open('dict/bad', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'bad')
    
with codecs.open('dict/normal', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'normal')
    
with codecs.open('dict/good', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'good')

with codecs.open('dict/bad', 'w', 'gb18030') as f_in:
    write_file(f_in, d, 'bad')
    
with codecs.open('dict/normal', 'w', 'gb18030') as f_in:
    write_file(f_in, d, 'normal')
    
with codecs.open('dict/good', 'w', 'gb18030') as f_in:
    write_file(f_in, d, 'good')

print 'All finished!'

