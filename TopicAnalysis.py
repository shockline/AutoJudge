import codecs
import string

import numpy as np



question = ''
topic_dict = dict()

with codecs.open('otherdata/topic', 'r', 'gb18030') as fin:
    for line in fin:
        line = line.strip()
        if '<END>' in line:
            tokens = line.split('\t')
            topic_id = string.atoi(tokens[1])
            topic_prob = string.atof(tokens[2])
            topic_dict[question][topic_id] = topic_prob
        else:
            question = line
            topic_dict[question] = dict()


question_topic_statistic_list = list()     
for question, question_dict in topic_dict.items():
    if len(question_dict) != 4:
        print 'wrong',
    prob_list = list(question_dict.values())
    
    prob_mean = np.mean(prob_list)
    prob_std = np.std(prob_list)
    
    question_topic_statistic_list.append((question, prob_mean, prob_std))
#     print '%s\t%f\t%f' % (question, prob_mean, prob_std)

sorted_res = sorted(question_topic_statistic_list, key=lambda x:x[1])
for question, prob_mean, prob_std in sorted_res:
    print '%s\t%f\t%f' % (question, prob_mean, prob_std)


print 'All finished!'
