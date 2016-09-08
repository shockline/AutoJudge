import codecs
import os

def read_file(f, d, label): 
    for line in f:
        line = line.strip()
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

file_list = os.listdir('judge/input') 
file_list = sorted(file_list)
for basename in file_list:
    if not os.path.isfile('judge/input/' + basename):
        continue
    
    count_dict = dict()
    count_dict['good'] = 0
    count_dict['bad'] = 0
    count_dict['normal'] = 0
    count_dict['unknown'] = 0
    
    response_per_input = 5
    
    top_acc = [0] * response_per_input
    top_error = [0] * response_per_input
    not_bad_group_count = 0
    group_count = 0
    not_bad = False
    with codecs.open('judge/input/' + basename, 'r', 'gb18030') as f_in:
        with codecs.open('judge/output/' + basename, 'w', 'gb18030') as f_out:
            with codecs.open('judge/unknown/' + basename, 'w', 'gb18030') as f_out_unkonwn:
                key = ''
                unknonwn_key = ''
                value = ''
                
                question_count = 0
                
                for line in f_in:
                    line = line.strip().replace(' ', '')
                    if len(line) == 0:
                        continue
                    if not '<END>' in line and not '<START>' in line and not 'result' in line:
                        if '\t' in line:
                            tt = line.find('\t')
                            key = line[:tt]
                        else:
                            key = line
                        f_out.write('%s\n' % key)
                        question_count = 0
                        group_count += 1
                        if not_bad:
                            not_bad_group_count += 1
                        not_bad = False
                    else:
                        if '<START>' in line:
                            start_index = line.find('<START>') + len('<START>')
                            end_index = line.rfind('<EOF>')
                        elif '<END>' in line:
                            start_index = line.find('<END>') + len('<END>')
                            end_index = line.rfind('<END>')
                        else:
                            start_index = line.find('result: ') + len('result: ')
                            end_index = line.find('|')                            
                        v = line[start_index:end_index].strip()
                        if (key, v) in d:
                            label = d[(key, v)]
                        else:
                            label = 'unknown'
                        
                        if label == 'good' or label == 'normal':
                            not_bad = True
                            for i in xrange(question_count, response_per_input):
                                top_acc[i] += 1
                        else:
                            for i in xrange(question_count, response_per_input):
                                top_error[i] += 1
                                    
                                
                        
                        count_dict[label] += 1
                        f_out.write('<END>%s<END>\t%s\n' % (v, label))
                        if label == 'unknown':
                            if unknonwn_key != key:
                                unknonwn_key = key
                                f_out_unkonwn.write('%s\n' % unknonwn_key)
                            f_out_unkonwn.write('<END>%s<END>\n' % v)
                        
                        question_count += 1
    
    total_data_count = count_dict['bad'] + count_dict['normal'] + count_dict['good']
    
    print '%s:' % basename
    for k, v in count_dict.items():
        print '%s\t%d' % (k, v)
    for i, (acc, error) in enumerate(zip(top_acc, top_error)):
        print 'top %d acc: \t%f' % (i, acc / 1.0 / (acc + error))
    print 'Bad Rate:\t%f' % (count_dict['bad'] / 1.0 / total_data_count)
    print 'Normal Rate:\t%f' % (count_dict['normal'] / 1.0 / total_data_count)
    print 'Good Rate:\t%f' % (count_dict['good'] / 1.0 / total_data_count)
    print 'Not bad group Rate:\t%f' % (not_bad_group_count / 1.0 / group_count)
    print
print 'All finished!'                   
                    
            
    
