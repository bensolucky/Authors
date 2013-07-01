"""
This program reads a csv of author names and frequencies of the pieces of
those names.  It also reads in pre-processed affiliations and "author groups",
which are authors that are listed for 2 papers of the same title.

It then groups authors by Last Name / First Initial and forms duplicate
groups based on the above information
"""
import pandas as pd
import numpy as np
import util
from sets import Set
authors = pd.read_csv("freq54.csv", index_col=0)

# joint frequency of names
authors['first_last_freq'] = authors['last_freq'] * authors['first_freq']
authors['firsts_last_freq'] = authors['last_freq'] * authors['firsts_freq']
authors['nick_last_freq'] = authors['last_freq'] * authors['nick_freq']
authors['nicks_last_freq'] = authors['last_freq'] * authors['nicks_freq']
authors['fi_last_freq'] = authors['last_freq'] * authors['fi_freq']

# This fixes a problem in read.csv (pandas reads "Nan" as missing)
authors['Last'][pd.isnull(authors['Last'])] = "nan"
authors['First'][pd.isnull(authors['First'])] = "nan"
authors['Firsts'][pd.isnull(authors['Firsts'])] = "nan"
authors['Nick'][pd.isnull(authors['Nick'])] = "nan"
authors['Nicks'][pd.isnull(authors['Nicks'])] = "nan"
authors['FILastName'] = authors['FI'] + authors['Last']

# These are some stray nicknames that I noticed at the last minute,
# these would normally be handled in parse_and_count.py
authors['Nick'][authors['Nick']=='andrey'] = "andre"
authors['Nicks'][authors['Nicks']=='andrey'] = "andre"

# Make the Last name / First Initial groups
groups = authors.groupby(['FILastName'])

# This file, keyed on AuthorID, only contains authors with PaperAuthor records.
papers = pd.read_csv("Author2.csv", index_col=0)
# Reading in the parsed affiliations and the author groups
affs = util.read_tsv_of_lists("affs_loose.tsv", "Affiliation")
agrps = util.read_tsv_of_lists("Author8a6.tsv", "agrps")

# Function to decide if 2 middle names could be from the same author
# Middle names have been stored with "." as a word seperator
def check_mids(str1, str2):
    if str1[0] == str2[0]:
        # This if catches First M. Last and First Middle Last pairs
	if len(str1) == 1 or len (str2) == 1:
	    return 1
        # This if catches middle names that differ only in whitespace
        elif str1.replace('.', '') == str2.replace('.', ''):
	    return 1
    # This block catches middle names where the same word appears in both
    pieces1 = str1.split('.')
    pieces2 = str2.split('.')
    for p1 in pieces1:
        if len(p1) > 1 and p1 in pieces2:
            return 1
    # This catches middle names that are spelled similary. An example would
    # be: First Middle Last and First Midle Last
    if len(str1) > 3 and len(str2) > 3:
	if str1[-4:] == str2[-4:]: # print these
	    return 1
        elif str1[:4] == str2[:4]:
	    return 1
        elif str1[:3] == str2[:3]:
	    return 1
    # This catches abbreviated multiple-word middle names.
    # First A.B.C Last and First Al Ben Chad Last, for example
    if len(pieces1) > 1 and len(pieces2) > 1:
        abbr1 = ""
        abbr2 = ""
        for p1 in pieces1:
	    abbr1 += p1[0]
        for p2 in pieces2:
	    abbr2 += p2[0]
        if abbr1[0:2] == abbr2[0:2]:
	    return 1
    return 0

# Check if 2 authors share any affiliation words in common, or are in the same author group
def checks(aid1, aid2):
    if aid1 in affs.index and aid2 in affs.index and util.check_affs(affs['Affiliation'][aid1], affs['Affiliation'][aid2]):
        return 1
    elif aid1 in agrps.index and aid2 in agrps.index and util.check_conf(agrps['agrps'][aid1], agrps['agrps'][aid2]):
        return 1
    return 0

# These are cutoffs to filter duplicates based on joint frequency of name pieces.
Fullcutoff = 32000
NoMidcutoff1 = 23000
NoMidcutoff2 = 99999
NoMidcutoff3 = 78000
MIcutoff = 22000  

# De-bugging / Reporting variables
countA, countB, countC = 0,0,0
counta, countb, countc = 0,0,0
countG, countH, countI = 0,0,0
countg, counth, counti = 0,0,0
countD, countE, countF = 0,0,0
countd, counte, countf = 0,0,0
countx, county = 0,0

f = open('54.csv', 'w')
print >>f, "AuthorId,DuplicateAuthorIds"
"""
The next loop of code could be confusing.  I'll describe the general logc.
I begin with each group of athors who share a last name and first inital.  
Within that, each type of commonality as a seperate case.  Some pairs of 
authors have the exact same name, others have a similar first name or a 
similar middle initial.  Or maybe they have the same first name but one
is missing a middle nmae.  Each case is handled a little differently.

But in general, these different treatments are similar.  I take the joint
frequency of the least specific common parts of the 2 names, for instance
F Last and First Last - I'll take the frequency of F Last.  Or First M Last
and First Last I would take First Last.  I then usually count the number of
times that the other name appears and I divide the frequency by the count 
and allow the duplicate if it is under a certain threshold. More common
"joint frequencies" are more likely to be false duplicates.

The idea is that a very common first and last name is less likely to be a true
duplcate.  If the first name of one member of a pair is only a first initial, 
than it is a very common "name" indeed.  "J Fisher" could match with "Jay
Fisher" or "Jason Fisher".  But of the 2 I would prefer that "J Fisher 
matches with the more common specific name between "Jay" and "Jason".  For 
instance there are many records of "Albert Einstein" in the data.  There could
also be a single record of "Alonzo Einstein".  I would like to match any 
"A Einstein" with the former, not the latter. 
"""
# Each group is made of all authors with the same last name and same first initial
for name, group in groups:
    for id in group.index:
	f.write(str(id) + ",")
	# If an author is not in PaperAuthors, it has no duplicates
	if id not in papers.index:
	    print >>f, id,
	# If the name is flagged as missing, it has no dupes
	elif name == 'mmissing':
	    print >>f, id,
	# Otherwise, check against the other authors in the group
	else:
	    for dupe in group.index:
		if dupe == id:
		    print >>f, id,
 		elif dupe not in papers.index:
 		    continue
	        ####################### Same First Name Block ######################
	        # First check cases where the first names are identical:
	        elif group['First'][id] == group['First'][dupe]:
                    ##################### Same Middle ##############################
		    if group['Name'][id] == group['Name'][dupe]:
			countA += 1
			if checks(id, dupe):
  			    counta += 1
			    print >>f, dupe,
			elif group['firsts_last_freq'][id] / len(group.index[group['Name']==group['Name'][id]]) < Fullcutoff:
			    counta += 1
			    print >>f, dupe,
                    ################## 1 Middle Name Missing #####################
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
			    countb += 1
			    print >>f, dupe,
                    ################## Similar Middle Names   #####################
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
	        #################### End Same First Name Block ######################

	        ####################### Same Nick Name Block## ######################
                # This section looks at authors whose first names could be nicknames or misspellings of each other
		# The logic is effectively identical to the above "same first name" block, but catches cases
		# like Tony/Anthony Last, or Ben/Benjamin Last, or Philip/Phillip Last, for example
	        elif group['Nick'][id] == group['Nick'][dupe]:
                    ##################### Same Middle ##############################
		    if group['Nicks'][id] == group['Nicks'][dupe]:
			countG += 1
			if checks(id, dupe):
  			    countg += 1
			    print >>f, dupe,
			elif group['nicks_last_freq'][id] / len(group.index[group['Name']==group['Name'][id]]) < Fullcutoff: 
			    countg += 1
			    print >>f, dupe,
                    ################## 1 Middle Name Missing #####################
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
			    counth += 1
			    print >>f, dupe,
                    ################## Similar Middle Names   #####################
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
	        ################### End Same Nick Name Block ########################

	        ################### Same First Inital Block #########################
		elif group['First'][id].__len__()==1 or group['First'][dupe].__len__()==1:
                    ##################### Same Middle ##############################
		    """
                    Here I do something a little different, a name like F. Last may have many
		    possible matches. The uniques variable below is used to count how many
		    different first names are associated with this FI Last combo. 
		    """
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
			else:
                            uniques = len(set(group['Nick'][pd.isnull(group['Mids'])].values))
			    if (uniques * freq / grp_len) < (2 * Fullcutoff):
	                        countd += 1
	                        print >>f, dupe,
                    ################## 1 Middle Name Missing #####################
		    elif pd.isnull(group['Mids'][id]) or pd.isnull(group['Mids'][dupe]):
			countE += 1
		        if group['first_last_freq'][id] > group['first_last_freq'][dupe]:
		    	    freq = group['first_last_freq'][id]
			    grp_len = len(group.index[group['Nicks']==group['Nicks'][dupe]])
			else:
			    freq = group['first_last_freq'][dupe]
			    grp_len = len(group.index[group['Nicks']==group['Nicks'][id]])
			# Because many (incorrectly) named authors start with "a" as a prepositions (in most 
			# cases this appears to be the result of the paper title given as the authors name), "a"
			# is over-estimated as a first initial / first name.  It occurs to me now that I should
			# have handled this more generally and in the parse_and_count.py program
			if group['FI'][id] == "a":
			    freq = freq / 3
			if checks(id, dupe):
  			    counte += 1
			    print >>f, dupe,
			else:
			    # nlgratio: the idea here is to look at the proportion of names with this last name that have this
			    # first initial to the ones that do not.  If most of the authors with this last name have this same
			    # first initial, than I believe they are more likely to be duplicates of one another.  I also think
			    # this has more to do with data leakage than with any property of names that is likely to generalize
			    num_last = group['last_freq'][id]
			    grp_size = len(group.index)
			    nlgratio = np.sqrt(float(num_last) / float(grp_size))
			    # These 2 blocks are cases like F Last and F Middle Last
			    if pd.isnull(group['Mids'][id]) and group['First'][id].__len__()==1:
				# Los and Cartwright are two names that I noticed did not appear to be good fits for the last set 
				# of metrics I was using...there were multiple authors being matched by the algo that were clearly
				# not matches for those last names
			        if nlgratio * (freq / grp_len) < NoMidcutoff2 and group['Last'][id] not in ['los', 'cartwright']:
	                            counte += 1
				    countx += 1
	                            print >>f, dupe,
		            elif pd.isnull(group['Mids'][dupe]) and group['First'][dupe].__len__()==1:
			        if nlgratio * (freq / grp_len) < NoMidcutoff2 and group['Last'][id] not in ['los', 'cartwright']:
	                            counte += 1
				    countx += 1
	                            print >>f, dupe,
		            # These 2 are cases like First Last and First Middle Last
		            elif pd.notnull(group['Mids'][id]) and group['First'][id].__len__()==1:
			        if nlgratio * (freq / grp_len) < NoMidcutoff3:
	                            counte += 1
				    county += 1
	                            print >>f, dupe,
		            elif pd.notnull(group['Mids'][dupe]) and group['First'][dupe].__len__()==1:
			        if nlgratio * (freq / grp_len) < NoMidcutoff3:
	                            counte += 1
				    county += 1
	                            print >>f, dupe,
                    ################## Similar Middle Names   #####################
		    elif group['First'][id].__len__()==1 or group['First'][dupe].__len__()==1:
			# First check if the middle names are similar enough
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
	        ################### End Same First Inital Block ######################
	print >>f
# Print some reporting / debugging numbers
print countA, countB, countC
print counta, countb, countc
print countG, countH, countI
print countg, counth, counti
print countD, countE, countF
print countd, counte, countf
print countx, county
f.close()
