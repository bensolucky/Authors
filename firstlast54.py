##########################################################################################################################
import pandas as pd
import numpy as np
import sys
import util
from sets import Set
authors = pd.read_csv("freq54.csv", index_col=0)
# joint frequency of names
authors['first_last_freq'] = authors['last_freq'] * authors['first_freq']
authors['firsts_last_freq'] = authors['last_freq'] * authors['firsts_freq']
authors['nick_last_freq'] = authors['last_freq'] * authors['nick_freq']
authors['nicks_last_freq'] = authors['last_freq'] * authors['nicks_freq']
authors['fi_last_freq'] = authors['last_freq'] * authors['fi_freq']
# Fixes a problem that occurs when you read the file in from csv (pandas read "Nan" as missing)
authors['Last'][pd.isnull(authors['Last'])] = "nan"
authors['First'][pd.isnull(authors['First'])] = "nan"
authors['Firsts'][pd.isnull(authors['Firsts'])] = "nan"
authors['Nick'][pd.isnull(authors['Nick'])] = "nan"
authors['Nicks'][pd.isnull(authors['Nicks'])] = "nan"
authors['FILastName'] = authors['FI'] + authors['Last']

authors['Nick'][authors['Nick']=='andrey'] = "andre"
authors['Nicks'][authors['Nicks']=='andrey'] = "andre"

groups = authors.groupby(['FILastName'])
papers = pd.read_csv("Author2.csv", index_col=0)
affs = util.read_tsv_of_lists("affs_loose.tsv", "Affiliation") # change to 4
agrps = util.read_tsv_of_lists("Author8a6.tsv", "agrps")

def check_mids(str1, str2):
    if str1[0] == str2[0]:
	if len(str1) == 1 or len (str2) == 1:
	    return 1
        elif str1.replace('.', '') == str2.replace('.', ''):
	    return 1
    pieces1 = str1.split('.')
    pieces2 = str2.split('.')
    for p1 in pieces1:
        if len(p1) > 1 and p1 in pieces2:
            return 1
    if len(str1) > 3 and len(str2) > 3:
	if str1[-4:] == str2[-4:]: # print these
	    return 1
        elif str1[:4] == str2[:4]:
	    return 1
        elif str1[:3] == str2[:3]:
	    return 1
    if len(pieces1) > 1 and len(pieces2) > 1:
        abbr1 = ""
        abbr2 = ""
        for p1 in pieces1:
	    abbr1 += p1[0]
        for p2 in pieces2:
	    abbr2 += p2[0]
        if abbr1[0:2] == abbr2[0:2]:
	    return 1
    #print str1, "\t\t", str2
    return 0

def checks(aid1, aid2):
    if aid1 in affs.index and aid2 in affs.index and util.check_affs(affs['Affiliation'][aid1], affs['Affiliation'][aid2]):
        return 1
    elif aid1 in agrps.index and aid2 in agrps.index and util.check_conf(agrps['agrps'][aid1], agrps['agrps'][aid2]):
        return 1
    return 0

# set these to be a couple billion to run "greedy" mode
Fullcutoff = 32000
NoMidcutoff1 = 23000
NoMidcutoff2 = 25000
MIcutoff = 22000  
#Fullcutoff = 999999999999999
#NoMidcutoff = 999999999999999
#MIcutoff = 999999999999999999

countA, countB, countC = 0,0,0
counta, countb, countc = 0,0,0
countG, countH, countI = 0,0,0
countg, counth, counti = 0,0,0
countD, countE, countF = 0,0,0
countd, counte, countf = 0,0,0
countx, county = 0,0
f = open('54.csv', 'w')
print >>f, "AuthorId,DuplicateAuthorIds"
for name, group in groups:
    for id in group.index:
	f.write(str(id) + ",")
	if id not in papers.index:
	    print >>f, id,
	elif name == 'mmissing': # can I subtract this line?
	    print >>f, id,
	else:
	    for dupe in group.index:
		if dupe == id:
		    print >>f, id,
 		elif dupe not in papers.index:
 		    continue
	        elif group['First'][id] == group['First'][dupe]:
		    if group['Name'][id] == group['Name'][dupe]:
			countA += 1
			if checks(id, dupe):
  			    counta += 1
			    print >>f, dupe,
			elif group['firsts_last_freq'][id] / len(group.index[group['Name']==group['Name'][id]]) < Fullcutoff:
			    counta += 1
			    print >>f, dupe,
	            # could put unique here too (where first == first)
		    elif pd.isnull(group['Mids'][id]) or pd.isnull(group['Mids'][dupe]):
			countB += 1
		        if pd.isnull(group['Mids'][id]):
		    	    freq = group['first_last_freq'][id]
			    grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			else:
			    freq = group['first_last_freq'][dupe]
			    grp_len = len(group.index[group['Name']==group['Name'][id]])
			if checks(id, dupe):
  			    countb += 1
			    print >>f, dupe,
			elif (freq / grp_len) < NoMidcutoff1:
			    #print "in: ", group['Name'][id],  group['Name'][dupe], freq / grp_len
			    countb += 1
			    print >>f, dupe,
			#else:
			    #print "out: ", group['Name'][id],  group['Name'][dupe], freq / grp_len
	            elif check_mids(group['Mids'][id], group['Mids'][dupe]) == 1:
		        countC += 1
		        if group['firsts_last_freq'][id] > group['firsts_last_freq'][dupe]:
		    	    freq = group['firsts_last_freq'][id]
			    grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			else:
			    freq = group['firsts_last_freq'][dupe]
			    grp_len = len(group.index[group['Name']==group['Name'][id]])
			if checks(id, dupe):
  			    countc += 1
			    print >>f, dupe,
			elif (freq / grp_len) < MIcutoff:
			    countc += 1
			    print >>f, dupe,
# Nicknamess
	        elif group['Nick'][id] == group['Nick'][dupe]:
		    if group['Nicks'][id] == group['Nicks'][dupe]:
			countG += 1
			if checks(id, dupe):
  			    countg += 1
			    print >>f, dupe,
			elif group['nicks_last_freq'][id] / len(group.index[group['Name']==group['Name'][id]]) < Fullcutoff: 
			    countg += 1
			    print >>f, dupe,
		    elif pd.isnull(group['Mids'][id]) or pd.isnull(group['Mids'][dupe]):
			countH += 1
		        if pd.isnull(group['Mids'][id]):
		    	    freq = group['nick_last_freq'][id]
			    grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			else:
			    freq = group['nick_last_freq'][dupe]
			    grp_len = len(group.index[group['Name']==group['Name'][id]])
			if checks(id, dupe):
  			    counth += 1
			    print >>f, dupe,
			elif (freq / grp_len) < NoMidcutoff1:
			    #print "in: ", group['Name'][id],  group['Name'][dupe], freq / grp_len
			    counth += 1
			    print >>f, dupe,
			#else:
			    #print "out: ", group['Name'][id],  group['Name'][dupe], freq / grp_len
	            elif check_mids(group['Mids'][id], group['Mids'][dupe]) == 1:
		        countI += 1
		        if group['nicks_last_freq'][id] > group['nicks_last_freq'][dupe]:
		    	    freq = group['nicks_last_freq'][id]
			    grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			else:
			    freq = group['nicks_last_freq'][dupe]
			    grp_len = len(group.index[group['Name']==group['Name'][id]])
			if checks(id, dupe):
  			    counti += 1
			    print >>f, dupe,
			elif (freq / grp_len) < MIcutoff:
			    counti += 1
			    print >>f, dupe,
# FI
		elif group['First'][id].__len__()==1 or group['First'][dupe].__len__()==1:
		    if group['Mids'][id] == group['Mids'][dupe] or (pd.isnull(group['Mids'][id]) and pd.isnull(group['Mids'][dupe])):
			countD += 1
		        if group['firsts_last_freq'][id] > group['firsts_last_freq'][dupe]:
		    	    freq = group['firsts_last_freq'][id]
			    grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			else:
			    freq = group['firsts_last_freq'][dupe]
			    grp_len = len(group.index[group['Name']==group['Name'][id]])
			if checks(id, dupe):
      			    countd += 1
    			    print >>f, dupe,
		        elif group['Mids'][id] == group['Mids'][dupe]:
		            if (freq / grp_len) <  Fullcutoff:
	                        countd += 1
	                        print >>f, dupe,
			    #else:
			    #    print "out1 ", group['Name'][id], "\t", group['Name'][dupe], freq/grp_len
			else:
                            uniques = len(set(group['Nick'][pd.isnull(group['Mids'])].values))
			    if (uniques * freq / grp_len) < (2 * Fullcutoff):
	                        countd += 1
	                        print >>f, dupe,


# Work on HERE
		    elif pd.isnull(group['Mids'][id]) or pd.isnull(group['Mids'][dupe]):
			countE += 1
		        if group['first_last_freq'][id] > group['first_last_freq'][dupe]:
		    	    freq = group['first_last_freq'][id]
			    grp_len = len(group.index[group['Nicks']==group['Nicks'][dupe]])
			else:
			    freq = group['first_last_freq'][dupe]
			    grp_len = len(group.index[group['Nicks']==group['Nicks'][id]])
			if group['FI'][id] == "a":
			    freq = freq / 3
			if checks(id, dupe):
  			    counte += 1
			    print >>f, dupe,
			else:
			    num_last = group['last_freq'][id]
			    grp_size = len(group.index)
			    nlgratio = np.sqrt(float(num_last) / float(grp_size))
			    if pd.isnull(group['Mids'][id]) and group['First'][id].__len__()==1:         # j smith and jake blah smith
			        if nlgratio * (freq / grp_len) < 99999 and group['Last'][id] not in ['los', 'cartwright']:
	                            counte += 1
				    countx += 1
	                            print >>f, dupe,
			        #elif (freq/grp_len < 121000):
			        #    print "out1 ", int(nlgratio * (freq / grp_len)), group['Name'][id], "\t", group['Name'][dupe], "\t", freq/grp_len, num_last, grp_size
		            elif pd.isnull(group['Mids'][dupe]) and group['First'][dupe].__len__()==1:
			        if nlgratio * (freq / grp_len) < 99999 and group['Last'][id] not in ['los', 'cartwright']:
	                            counte += 1
				    countx += 1
	                            print >>f, dupe,
			        #elif (freq/grp_len < 121000):
			        #    print "out1 ", int(nlgratio * (freq / grp_len)), group['Name'][id], "\t", group['Name'][dupe], "\t", freq/grp_len, num_last, grp_size
		            elif pd.notnull(group['Mids'][id]) and group['First'][id].__len__()==1:      # j blah smith and jake smith
			        if nlgratio * (freq / grp_len) < 78000:
	                            counte += 1
				    county += 1
	                            print >>f, dupe,
			        elif nlgratio * (freq / grp_len) < 118000:
			            print "out2 ", int(nlgratio * (freq / grp_len)), group['Name'][id], "\t", group['Name'][dupe], "\t", freq/grp_len, num_last, grp_size
		            elif pd.notnull(group['Mids'][dupe]) and group['First'][dupe].__len__()==1:
			        if nlgratio * (freq / grp_len) < 78000:
	                            counte += 1
				    county += 1
	                            print >>f, dupe,
			        elif  nlgratio * (freq / grp_len)< 118000:
			            print "out2 ", int(nlgratio * (freq / grp_len)), group['Name'][id], "\t", group['Name'][dupe], "\t", freq/grp_len, num_last, grp_size





		    elif group['First'][id].__len__()==1 or group['First'][dupe].__len__()==1:
	                if check_mids(group['Mids'][id], group['Mids'][dupe]) == 1:
			    countF += 1
		            if group['firsts_last_freq'][id] > group['firsts_last_freq'][dupe]:
		    	        freq = group['firsts_last_freq'][id]                            
			        grp_len = len(group.index[group['Name']==group['Name'][dupe]])
			    else:
			        freq = group['firsts_last_freq'][dupe]                        
			        grp_len = len(group.index[group['Name']==group['Name'][id]]) 
			    if checks(id, dupe):
  			        countf += 1
			        print >>f, dupe,
			    elif (freq / grp_len) < MIcutoff: 
			        countf += 1
			        print >>f, dupe,
			    #else:
			    #    print "out: ", group['Name'][id],  group['Name'][dupe], freq/grp_len
	print >>f
print countA, countB, countC
print counta, countb, countc
print countG, countH, countI
print countg, counth, counti
print countD, countE, countF
print countd, counte, countf
print countx, county
f.close()
