import pandas as pd
import re
import os
import multiprocessing
import math
import matplotlib.pyplot as plt

def get_status_corpus(user_status):
	# agg = dict(list(user_status.dropna().groupby('userid')))
	# num_users = len(agg)

	# user_index_to_id = {}
	# counter = 0
	# lis = []
	# for i,row in agg.iteritems():

	# 	user_index_to_id[counter] = i
	# 	counter +=1
	# 	lis.append(" ".join(list(row['status_update'])))
	     
	# print 'Number of users is ', num_users
	# return lis,user_index_to_id
	statuses =  list(user_status['status_update'])

	corpus = []
	for i in xrange(len(statuses)):
		status = statuses[i]
		
		if isinstance(status, str) :
			status = re.sub(r'[^a-zA-Z0-9!?,.\s]', '', status)
			#status = re.sub(r'([a-z])\1\1+', r'\1', status)
			status = status.lower()
			cur=status.split()
			corpus.append(cur)
		# else:
		# 	print status
	return corpus

f = open('data/rnn_input', 'w')
dictionary={}
user_status = pd.read_csv(os.path.join('data', 'sample_status'), sep = ',')#, escapechar = '/', quotechar='"')
statuses = get_status_corpus(user_status)
print 'data cleaning done'
total=0
idx = 0
for status in statuses:
	idx += 1
	if idx % 10000 == 0:
		print idx
        f.write('-DOCSTART-'+'\n')
        for term in status:
		punctuation = ''
		if term[-1] == '!' or term[-1] == '?' or term[-1] == '.' or term[-1] == ',':
			punctuation = term[-1]
		term = re.sub(r'[^a-zA-Z0-9\s]', '', term)
		if term != '':
			f.write(term + '\n')
			total += 1
			if not term in dictionary:
				dictionary[term] = 1
			else:
				dictionary[term] += 1
		if punctuation != '':
			f.write(punctuation + '\n')
			total += 1
			if not punctuation in dictionary:
				dictionary[punctuation] = 1
			else:
				dictionary[punctuation] += 1


                #b=''
                #c=''
                #for i in term:
                #        if i.isalpha() or i.isdigit():
                #                b+=i
                #        else:
                #                c+=i
                #if b!='':
                #        f.write(b+'\n')
                #        total+=1
                #        if not b in dictionary.keys():
                #                dictionary[b]=1
                #        else:
                #                dictionary[b]=dictionary[b]+1
                #if c!='':
                #        f.write(c+'\n')
                #        total+=1
                #        if not c in dictionary.keys():
                #                dictionary[c]=1
                #        else:
                #                dictionary[c]=dictionary[c]+1
f.close()
print total
import operator
########################################
#number of our terms 5273
#minimal occurrence 200
#number of total tokens 58500634
#number of our tokens 53865533
minimal_occurrence = 500
f = open('data/dictionary', 'w')
fp = open('data/dictionary_other', 'w')

#x=[]
#count=0
#import operator
#dict_sort = sorted(dictionary.items(), key=operator.itemgetter(1),reverse=True)
#for (term,termcount) in dict_sort:
#        f.write(term)
#        f.write(' '+(str)(termcount))
#        f.write(' '+(str)(((float)(termcount)/(float)(total)))+'\n')
#        count=count+1
#        x.append((count,termcount))
#f.close()
#plt.plot(*zip(*x))
x = {}

origin = dictionary
dictionary = {term:termcount for (term, termcount) in dictionary.items() if termcount >= minimal_occurrence}

for (term, termcount) in dictionary.items():
	if termcount in x:
		x[termcount] += 1
	else:
		x[termcount] = 1
dict_sort = sorted(dictionary.items(), key=operator.itemgetter(1),reverse=True)

for (term, termcount) in dict_sort:
	f.write(term)
	f.write(' '+(str)(termcount))
	f.write(' '+(str)(((float)(termcount)/(float)(total)))+'\n')

for (term, termcount) in origin.items():
	if term not in dictionary:
		fp.write(term)
		fp.write(' '+(str)(termcount))
		fp.write(' '+(str)(((float)(termcount)/(float)(total)))+'\n')


fp.close()
f.close()
x = sorted(x.items(), key=operator.itemgetter(0), reverse=True)
print x
print sum([num for termcount, num in x])
print sum([termcount * num for termcount, num in x])


plt.bar(*zip(*x))

plt.show()
plt.savefig('data/dictionary.png')
