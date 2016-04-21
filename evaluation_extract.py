# coding=gbk

import sys
import os
import codecs
from collections import defaultdict

import xlrd

input_dir = 'xlsx/input/'

query_answers = defaultdict(list)
querys = set()
files = os.listdir(input_dir)
for f in files:
    if os.path.isfile(input_dir + '/' + f):
        data = xlrd.open_workbook(input_dir + '/' + f)
        sheets_len = len(data.sheets())
        print f
        for i in range(sheets_len):
            table = data.sheets()[i]
            print table.name
            nrows = table.nrows
            question = ''
            for j in range(nrows):
                query = table.cell(j, 0).value
                query = query.strip()
                label = str(table.cell(j, 1).value)
                if ('<END>' in query or '<START>' in query) and len(question) > 0:
                    if label == 'normal' or label == 'good' or label == 'bad':
                        if '<START>' in query:
                            start_index = query.find('<START>') + len('<START>')
                            end_index = query.rfind('<EOF>')
                        else:
                            start_index = query.find('<END>') + len('<END>')
                            end_index = query.rfind('<END>')
                        query = query[start_index:end_index].strip()
                        query_answers[label + '_case'].append(question + '\t' + query)
                        querys.add(question)
                    elif query.startswith('<END>') or query.startswith('<START>'):
                        continue
                else:
                    question = query.replace(' ', '')
                    
for item in query_answers:
    with codecs.open('xlsx/' + item + '.txt', 'w', 'gb18030') as fout:
        all_example = set()
        for item1 in query_answers[item]:
            query = item1.replace(' ', '')
            all_example.add(query)
        temp = defaultdict(list)
        for item1 in all_example:
            ss = item1.split('\t')
            temp[ss[0]].append(ss[1])
        for query in temp:
            for answer in temp[query]:
                fout.write('%s\t%s\n' % (query, answer))
                              
with codecs.open('xlsx/all_query.txt', 'w', 'gb18030') as fout:
    for item in querys:
        fout.write('%s\n' % item)

print 'All finished'
