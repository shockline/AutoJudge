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
        
d = dict()

with codecs.open('dict/bad', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'bad')
    
with codecs.open('dict/normal', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'normal')
    
with codecs.open('dict/good', 'r', 'gb18030') as f_in:
    read_file(f_in, d, 'good')

count_dict = dict()
count_dict['good'] = 0
count_dict['bad'] = 0
count_dict['normal'] = 0
count_dict['unknown'] = 0

with codecs.open('judge/input', 'r', 'gb18030') as f_in:
    with codecs.open('judge/output', 'w', 'gb18030') as f_out:
        with codecs.open('judge/unknown', 'w', 'gb18030') as f_out_unkonwn:
            key = ''
            unknonwn_key = ''
            value = ''
            
            for line in f_in:
                line = line.strip().replace(' ', '')
                if len(line) == 0:
                    continue
                if not '<END>' in line and not '<START>' in line:
                    key = line
                    f_out.write('%s\n' % key)
                else:
                    if '<START>' in line:
                        start_index = line.find('<START>') + len('<START>')
                        end_index = line.rfind('<EOF>')
                    else:
                        start_index = line.find('<END>') + len('<END>')
                        end_index = line.rfind('<END>')
                    v = line[start_index:end_index].strip()
                    if (key, v) in d:
                        label = d[(key, v)]
                    else:
                        label = 'unknown'
                    count_dict[label] += 1
                    f_out.write('%s\t%s\n' % (v, label))
                    if label == 'unknown':
                        if unknonwn_key != key:
                            unknonwn_key = key
                            f_out_unkonwn.write('%s\n' % unknonwn_key)
                        f_out_unkonwn.write('<END>%s<END>\n' % v)

for k, v in count_dict.items():
    print '%s\t%d' % (k, v)

print 'All finished!'                   
                    
            
    
