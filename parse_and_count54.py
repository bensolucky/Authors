"""
This code performs 3 major actions.  It first reads the names and corrects
simple issues, like non-english special characters and "jr" at the end of a name.
Then it does more complicated things, like searching for extra characters or
mis-ordered names.
Finally it counts the frequencies of the various portions of each author's name.
i.e., how many times their last name appears as a last name, etc... to be used
later

Important naming conventions are as follows:
	First: The first space-seperated piece of the author's name
	Last: The last piece
	Firsts: Everything except the last piece
	Mid: All but first and last
	Nick: a possible nickname or alternate spelling for a first name
	Nicks: Nick + Mid
"""
import pandas as pd
import sys
import numpy as np
import util
from util import dict_len
from util import dict_move
authors = pd.read_csv("Author.csv", index_col=0)
# A dataframe keyed on authorID and containing space-seperated affiliation words
affs = util.read_tsv_of_lists("affs_loose.tsv", "Affiliation")
####################################################################################
# Clean The Author names up a bit
####################################################################################
# Define Null names as the string "missing"
authors['Name'][pd.isnull(authors['Name'])] = 'missing'
# The next 4 lines are used later for cases that are like 
# "GW Bush" (First initial, Middle Initial, Last name).  I'm marking them here b/c
# initial capitalization is useful in later determining which 2 character first names
# are actually 2 initials
authors['GW Bush'] = 0
authors['GW Bush'][authors['Name'].str.contains("^[A-Z]{2} [A-Z][a-z]")] = 1 # 150 GW Bush 
authors['Gw Bush'] = 0
authors['Gw Bush'][authors['Name'].str.contains("^[A-Z][a-z] [A-Z][a-z]")] = 1 # 150 GW Bush 
# Parse Foreign Language Special Characters
authors['Name'] = authors['Name'].str.replace("^Jr\. ", "") # 46 # before lower-casing, remove Jr. at beggining of name
authors['Name'] = authors['Name'].str.lower()
authors['Name'] = authors['Name'].str.replace("\xe2\x80\x99", "'") #84 apostrophe
authors['Name'] = authors['Name'].str.replace("\xc2\xa8\xc2\xa2", "a") #32 Spanish a
authors['Name'] = authors['Name'].str.replace("\xc2\xa8", "") # 445 next character is an umlatts
authors['Name'] = authors['Name'].str.replace("\xc3\xa8", "e") # 19 French e
authors['Name'] = authors['Name'].str.replace("\xc3\xad", "i") # 73 Spanish i
authors['Name'] = authors['Name'].str.replace("\xc3\xa4", "a") # 66 German a
authors['Name'] = authors['Name'].str.replace("\xc3\xaa", "e") # 2 Portugese E
authors['Name'] = authors['Name'].str.replace("\xc3\xa3", "a") # 17 Portugese A
authors['Name'] = authors['Name'].str.replace("\xc3\xb3", "o") # 55 Portugese O
authors['Name'] = authors['Name'].str.replace("\xc3\xb6", "o") # 127 Swedish O
authors['Name'] = authors['Name'].str.replace("\xc3\x96", "o") # 13 Swedish o
authors['Name'] = authors['Name'].str.replace("\xc3\xaf", "i") # 3 Catalonian I
authors['Name'] = authors['Name'].str.replace("\xc3\xb8", "o") # 20 Icelandic O
authors['Name'] = authors['Name'].str.replace("\xc3\xba", "u") # 18 Catalonian u
authors['Name'] = authors['Name'].str.replace("\xc3\x85", "a") # 2 Norwegian A
authors['Name'] = authors['Name'].str.replace("\xc3\x89", "e") # 6 Swiss e
authors['Name'] = authors['Name'].str.replace("\xc3\xa9", "e") # 234 French e
authors['Name'] = authors['Name'].str.replace("\xc3\x9c", "u") # 5 Turkish U
authors['Name'] = authors['Name'].str.replace("\xc3\xbc", "u") # 109 German u
authors['Name'] = authors['Name'].str.replace("\xc3\xb1", "n") # 22 Spanish N
authors['Name'] = authors['Name'].str.replace("\xc3\xb4", "o") # 3 French O
authors['Name'] = authors['Name'].str.replace("\xc3\xa1", "a") # 105 Hungarian a
authors['Name'] = authors['Name'].str.replace("\xc3\xa7", "c") # 28 Portugese c
authors['Name'] = authors['Name'].str.replace("\xc3\x9f", "b") # 15 German B
authors['Name'] = authors['Name'].str.replace("\xc3\xb5", "o") # 16 Portugese o
authors['Name'] = authors['Name'].str.replace("\xc3\xa5", "a") # 4 Some? a
authors['Name'] = authors['Name'].str.replace("\xc3\xa0", "a") # 3 Some? a
authors['Name'] = authors['Name'].str.replace("\xc3\xab", "e") # 4 Some? e
authors['Name'] = authors['Name'].str.replace("\xc3\xb2", "o") # 1 Some? o
authors['Name'] = authors['Name'].str.replace("\xc5\x81", "l") # 4 Slavic L
authors['Name'] = authors['Name'].str.replace("\xc5\x82", "l") # 35 Slavic L
authors['Name'] = authors['Name'].str.replace(" \xc2\xb4 ", "")
authors['Name'] = authors['Name'].str.replace(" \xc2\xb4", "")
authors['Name'] = authors['Name'].str.replace("\xc2\xb4", "")
authors['Name'] = authors['Name'].str.replace("\xc2\xb8", "")
authors['Name'] = authors['Name'].str.replace("\xc2\xa6", "e")
authors['Name'] = authors['Name'].str.replace("\xc2\xaa", "i")
authors['Name'] = authors['Name'].str.replace("\xc4\xb1", "i")
authors['Name'] = authors['Name'].str.replace("\xc3\xb0", "d")
authors['Name'] = authors['Name'].str.replace("\xef\xbf\xbd", "e")
authors['Name'] = authors['Name'].str.replace("\xc3\x9a", "u")
# Remove Non-alphanumerics
authors['Name'] = authors['Name'].str.replace("~", "") # 24
authors['Name'] = authors['Name'].str.replace("`", "") # 24
authors['Name'] = authors['Name'].str.replace("|", "e") # 24
authors['Name'] = authors['Name'].str.replace("_", "") # 24
authors['Name'] = authors['Name'].str.replace("\\", "") # ??
authors['Name'] = authors['Name'].str.replace(" \(\w+\)", "") # ??
authors['Name'] = authors['Name'].str.replace(" \([a-z]+ [a-z]+\)", "") # ??
authors['Name'] = authors['Name'].str.replace(" \([a-z]+ [a-z]+ [a-z]+ [a-z]+\)", "") # ??
authors['Name'] = authors['Name'].str.replace("   ", "") # 35
authors['Name'] = authors['Name'].str.replace("  ", " ") # 67
authors['Name'] = authors['Name'].str.replace(",", " ") # 7
authors['Name'] = authors['Name'].str.replace("'", "") #1258
authors['Name'] = authors['Name'].str.replace("-", " ") # 15748
authors['Name'] = authors['Name'].str.replace(";", " ") # 15748
authors['Name'] = authors['Name'].str.replace("\. ", " ") # 115748
authors['Name'] = authors['Name'].str.replace("\.", " ") # 5281
authors['Name'] = authors['Name'].str.replace("\?", " ") # 5281
# Remove some titles that seem to create duplicates
authors['Name'] = authors['Name'].str.replace(" iii", "") # 188
authors['Name'] = authors['Name'].str.replace(" ii$", "") # 188
authors['Name'] = authors['Name'].str.replace(" iv$", "") # 188
authors['Name'] = authors['Name'].str.replace(" mbbs", "") # 188
authors['Name'] = authors['Name'].str.replace(" junior$", "") #
authors['Name'] = authors['Name'].str.rstrip()
authors['Name'] = authors['Name'].str.replace("jr$", "") #
# Change some specific names that look like duplicates for which I never found
# a more programatic method of changing
authors['Name'] = authors['Name'].str.replace("^bernd r t simonet", "bernd r t simoneit")
authors['Name'] = authors['Name'].str.replace("rafalw eron", "rafal weron")
authors['Name'] = authors['Name'].str.replace("rafaascherer", "rafal scherer")
authors['Name'] = authors['Name'].str.replace("rafaa scherer", "rafal scherer")
authors['Name'] = authors['Name'].str.replace("a lagendijk", "ad lagendijk")
authors['Name'] = authors['Name'].str.replace("gsmje", "guus")
authors['Name'] = authors['Name'].str.replace("philippe", "philipe")
# These are some words that are occasionally mistakenly tacked onto a name
authors['Name'] = authors['Name'].str.replace(" faculty", "")
authors['Name'] = authors['Name'].str.replace("^llc ", "")
authors['Name'] = authors['Name'].str.replace(" information", "")
authors['Name'] = authors['Name'].str.replace(" revision", "")
authors['Name'] = authors['Name'].str.replace("cortex ", "")
authors['Name'] = authors['Name'].str.replace(" january", "")
authors['Name'] = authors['Name'].str.replace(" february", "")
authors['Name'] = authors['Name'].str.replace(" september", "")
authors['Name'] = authors['Name'].str.replace(" october", "")
authors['Name'] = authors['Name'].str.replace(" november", "")
authors['Name'] = authors['Name'].str.replace(" december", "")
authors['Name'] = authors['Name'].str.replace("  ", " ") # 537, not doing this can screw up some later code
authors['Name'] = authors['Name'].str.rstrip()
# These words all reliably indicate a name is just missing
authors['Name'][authors['Name'].str.contains("case stud")] = 'missing'
authors['Name'][authors['Name'].str.contains("^by ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^communicated ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^computer")] = 'missing'
authors['Name'][authors['Name'].str.contains("^for ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^from ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^the ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^inc ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^book ")] = 'missing'
authors['Name'][authors['Name'].str.contains("multi")] = 'missing'
authors['Name'][authors['Name'].str.contains("methods")] = 'missing'
authors['Name'][authors['Name'].str.contains("^high")] = 'missing'
authors['Name'][authors['Name'].str.contains("^including ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^includes ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^of ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^on ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^as ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^at ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^applied")] = 'missing'
authors['Name'][authors['Name'].str.contains(" number")] = 'missing'
authors['Name'][authors['Name'].str.contains("^correction")] = 'missing'
authors['Name'][authors['Name'].str.contains("^manufacturing")] = 'missing'
authors['Name'][authors['Name'].str.contains("^optimization ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^program ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^processing ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^process ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^revised ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^and ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^scal")] = 'missing'
authors['Name'][authors['Name'].str.contains("^we ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^with ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^prof ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^proffessor ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^ph d ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^real")] = 'missing'
authors['Name'][authors['Name'].str.contains("^series ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^three ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^through")] = 'missing'
authors['Name'][authors['Name'].str.contains("^toward")] = 'missing'
authors['Name'][authors['Name'].str.contains("^what ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^when ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^where ")] = 'missing'
authors['Name'][authors['Name'].str.contains("theory$")] = 'missing'
authors['Name'][authors['Name'].str.contains("workshop")] = 'missing'
authors['Name'][authors['Name'].str.contains("vol no")] = 'missing'
authors['Name'][authors['Name'].str.contains("statistics")] = 'missing'
authors['Name'][authors['Name'].str.contains("technology")] = 'missing'
authors['Name'][authors['Name'].str.contains("results")] = 'missing'
authors['Name'][authors['Name'].str.contains("^1 ")] = 'missing'
authors['Name'][authors['Name'].str.contains("^2 ")] = 'missing'
print len(authors['Name'][authors['Name']=='missing'])
# This will make it easier to later catch names with either of these spellings
authors['Name'] = authors['Name'].str.replace(" van de ", " vande ")
authors['Name'] = authors['Name'].str.replace(" van der ", " vander ")
authors['Name'] = authors['Name'].str.replace(" van den ", " vanden ")
####################################################################################
###################### Asian-Name Names ############################################
""" I initially designed this to catch "asian names" duplicates that are often in
the form FirstMid Last, First-Mid Last and/or First Mid Last.  But many non-asian 
names can also be found in 2 or more of those formats."""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['First'] = authors['Name'].str.split().str[0]    # First name only
ansm1, ansm2 = 0,0
names = set(authors['Name'].values)
for row in authors.index:
    if len(authors['Name'][row].split(" ")) < 3:
	continue
    # check it's not middle initial
    if authors['Name'][row].split()[1].__len__() == 1:
	continue
    # now, try smushing first two
    smushed = authors['First'][row] + authors['Name'][row].split()[1] + " " + " ".join(authors['Name'][row].split()[2:])
    smushed2 = " ".join(authors['Name'][row].split()[:-2]) + " " + authors['Name'][row].split()[-2] + authors['Last'][row]
    if smushed in names:
        ansm1 += 1
        authors['Name'][row] = smushed
    elif smushed2 in names:
        ansm2 += 1
        authors['Name'][row] = smushed2
print ansm1, ansm2
####################################################################################
# GW Bush becomes G W Bush
####################################################################################
""" In this block, any name that was initially of the form FM Last or Fm Last is 
considered for splitting into F M Last.  But I want to avoid splitting common first
names, like Ed, Jo, or In (korean).  The best way I found to do this was to count 
total occurances of these strings as first names in the author file, and only split
up the less common 2 word first names.  The logic got a little complet below to try
to properly sort all the edge cases"""
authors['First'] = authors['Name'].str.split().str[0]    # First name only

author_first_set = authors.groupby(['First']).groups
for row in authors.index[authors['GW Bush'] == 1]:
    if dict_len(author_first_set, authors['First'][row]) < 18:
        if authors['First'][row] not in ['tu', 'vu']:
            authors['Name'][row] = authors['Name'][row][0] + " " + authors['Name'][row][1:]
authors = authors.drop(['GW Bush'], axis=1)

for row in authors.index[authors['Gw Bush'] == 1]:
    if authors['First'][row].__len__() == 2:
        if (authors['First'][row][1] in ['a', 'e', 'i', 'o', 'u', 'l', 'g']
            and authors['First'][row][0] not in ['j', 'r']) \
            or (authors['First'][row][0] in ['a', 'e', 'i', 'o', 'u']
                and authors['First'][row][1] not in ['j', 'r', 'm']):
            if dict_len(author_first_set, authors['First'][row]) < 10:
                if authors['First'][row] != 'vu':
                    authors['Name'][row] = authors['Name'][row][0] + " " + authors['Name'][row][1:]
        else:
            if dict_len(author_first_set, authors['First'][row]) < 24:
                authors['Name'][row] = authors['Name'][row][0] + " " + authors['Name'][row][1:]
authors = authors.drop(['Gw Bush'], axis=1)
####################################################################################
# George Bush X and George Bus H
####################################################################################
""" Singles character last names are very suspicious.  I try to parse these mistakes
by stripping the last character or combining it with a middle initial.  In either 
case, if this change makes it the same as an already existing name the change is
allowed"""
sm0, ch1, ch2 = 0, 0, 0
authors['Last'] = authors['Name'].str.split().str[-1]
author_set = set(authors['Name'])
for row in authors.index:
    if authors['Last'][row].__len__() == 1:
	smushed = (authors['Name'][row][:-2] + authors['Name'][row][-1])
	chopped = authors['Name'][row][:-2]
	if author_set.__contains__(smushed):
	    authors['Name'][row] = smushed
	    sm0 += 1
	    author_set.add(smushed)
        else:
	    authors['Name'][row] = chopped
            ch1 += 1
	    author_set.add(chopped)
authors['Last'] = authors['Name'].str.split().str[-1]
for row in authors.index:
    if authors['Last'][row].__len__() == 1:
	chopped = authors['Name'][row][:-2]
        if authors['Name'][row].__len__() > 2:
	    authors['Name'][row] = chopped
            ch2 += 1
print sm0, ch1, ch2
###################################################################################
###################### Asian-Name Names ############################################
""" This is just like the first "Asian Names" block, but here I look at cases
where the 2nd portion of the name is a middle initial only.  """
authors['Last'] = authors['Name'].str.split().str[-1]
authors['First'] = authors['Name'].str.split().str[0]    # First name only
ansm3, ansm4 = 0, 0
author_set = authors.groupby(['Name']).groups
for row in authors.index:
    if len(authors['Name'][row].split()) != 3:
        continue
        # check it's middle initial
    if authors['Name'][row].split()[1].__len__() != 1:
        continue
        # now, try smushing first two
    smushed = authors['First'][row] + authors['Name'][row].split()[1] + " " + authors['Last'][row]
    smushed2 = authors['First'][row] + " " + authors['Name'][row].split()[1] + authors['Last'][row]
    if smushed in author_set and dict_len(author_set, authors['Name'][row]) <= dict_len(author_set, smushed):
        ansm3 += 1
        print smushed
        authors['Name'][row] = smushed
    elif smushed2 in author_set and dict_len(author_set, authors['Name'][row]) <= dict_len(author_set, smushed2):
        ansm4 += 1
        print smushed2
        authors['Name'][row] = smushed2
print ansm3, ansm4
###################################################################################
###################### Backwards Names ############################################
""" Here I search for names where Last and First have been reversed.  I go through
every 2 word name and check if the reversed name also exists.  I created a metric
based on the frequencies of the old name, the old first name as a first name, the 
old last name as a last name and the same frequencies of the new name.  This metric
was created by thinking through what these frequencies would look like for mistakes
and non-mistakes, then eyeballing results to refine it. Co-affiliation words were
also used in the metric.  The end result was to switch most proposed reversed names
but not all.  I used similar logic for several other tests in the remainder of this
program"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['First'] = authors['Name'].str.split().str[0]    # First name only
b1,b2=0,0 # count the number of reverals that are accepted, refused by the metric
authors['Rev'] = authors['Last'] + " " + authors['First'] # proposed name change
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['First']).groups
for row in authors.index:
    if len(authors['Name'][row].split()) != 2:
	continue
    if authors['Last'][row] == authors['First'][row]:
	continue
    if author_set. __contains__(authors['Rev'][row]):
	# count all values used in the test metrics
        num_name = float(dict_len(author_set, authors['Name'][row])) 
        new_name = float(dict_len(author_set, authors['Rev'][row]))
        num_last = float(dict_len(author_last_set, authors['Last'][row]))
        new_last = float(dict_len(author_last_set, authors['First'][row]))
        num_first = float(dict_len(author_first_set, authors['First'][row]))
        new_first = float(dict_len(author_first_set, authors['Last'][row]))
	name_ratio = (num_name / new_name)
	last_ratio = (num_last / new_last)
	first_ratio = (num_first / new_first)
	test_ratio = name_ratio * last_ratio * first_ratio
	# Here we check that the proposed name seems more likley to be the "true name" than the original.  If so, proceed.
	# Otherwise, we'll probably enter this condition when we come to the proposed name in the authors.index
	if test_ratio <= 1:
	    # The test metric
	    test = num_name * num_name * np.sqrt(name_ratio) * num_last * np.sqrt(last_ratio) * num_first * np.sqrt(first_ratio)
	    if row in affs.index:
		for row2 in authors.index[authors['Name']==authors['Rev'][row]]:
                    if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
			print "XXXXXXXX"
                        test = test / 100
	    # Don't reverse the name
	    if (test > 50):
		b2 += dict_len(author_set, authors['Name'][row])
	        print authors['Name'][row], "XXXXXXXXXXXXXXXXXX TOO RISKY", b1, b2, test
	    # Reverse the name
	    else:
		b1 += dict_len(author_set, authors['Name'][row])
		auth_idx = author_set.pop(authors['Name'][row])
		author_set[authors['Rev'][row]] = auth_idx + author_set[authors['Rev'][row]]
		first = authors['First'][row]
		last = authors['Last'][row]
                authors['First'][auth_idx] = last
                authors['Last'][auth_idx] = first
                authors['Name'][auth_idx] = authors['Rev'][row]
	        print authors['Name'][row]
authors = authors.drop(['Rev'], axis=1)
###################################################################################
# Strip out the da from Portugese names
authors['Name'] = authors['Name'].str.replace(" da ", "") 
###################################################################################
###################### First Middle Reversed ######################################
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names of the form Middle First Last"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1] # First and Middle and everything except last name
authors['Firsts'] = authors['Firsts'].str.join(' ')
authors['Mids'] = authors['Firsts'].str.split(" ").str[1:] # Everything except first and last name
authors['Mids'] = authors['Mids'].str.join(' ')
authors['First'] = authors['Name'].str.split().str[0]    # First name only
r1,r2=0,0
authors['NewFs'] = authors['Mids'] + " " + authors['First']
authors['NewN'] = authors['NewFs'] + " " + authors['Last']
authors['FL'] = authors['First'] + " " + authors['Last']
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
author_fl_set = authors.groupby(['FL']).groups
for row in authors.index:
    if len(authors['Name'][row].split()) != 3:
        continue
    if authors['NewFs'][row] == authors['Firsts'][row]:
        continue
    if authors['NewN'][row] in author_set:
        num_name = float(dict_len(author_set, authors['Name'][row])) #
        new_name = float(dict_len(author_set, authors['NewN'][row])) #
        num_last = float(dict_len(author_last_set, authors['Last'][row])) #
        num_first = float(dict_len(author_first_set, authors['Firsts'][row])) #
        new_first = float(dict_len(author_first_set, authors['NewFs'][row])) #
        num_fl = float(dict_len(author_fl_set, authors['FL'][row])) #
        name_ratio = (num_name / new_name)
        first_ratio = (num_first / new_first)
        test_ratio = name_ratio * first_ratio
        if test_ratio <= 1:
            test = num_name * np.sqrt(name_ratio) * num_first * np.sqrt(first_ratio) * np.sqrt(num_last) * num_fl
	    if row in affs.index:
		for row2 in authors.index[authors['Name']==authors['NewN'][row]]:
                    if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
			print "XXXXXXXXXX"
                        test = test / 100
            print int(test), "\t", int(num_name), int(new_name), "|", int(num_first), int(new_first), "|", int(num_last), "|", int(num_fl), "\t\t",
            if test > 202:
                r2 += 1
                print authors['Name'][row], "XXXXXXXXXXXXXXXXXX TOO RISKY", r1, r2, test
            else:
                r1 += 1
                dict_move(author_set, authors['Name'][row], authors['NewN'][row], row)
                dict_move(author_first_set, authors['Firsts'][row], authors['NewFs'][row], row)
                authors['Firsts'][row] = authors['NewFs'][row]
                authors['Name'][row] = authors['NewN'][row]
                print authors['Name'][row]
authors = authors.drop(['NewFs'], axis=1)
authors = authors.drop(['NewN'], axis=1)
authors = authors.drop(['FL'], axis=1)
####################################################################################
####################################################################################
###################### Strip 1 Character off the end
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names of the form First LastX where X is a stray character"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
c0,c1,c2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if author_set.__contains__(authors['Name'][row][:-1]):
        num_long_name = float(dict_len(author_set, authors['Name'][row]))
        num_shrt_name = float(dict_len(author_set, authors['Name'][row][:-1]))
        num_long_last = float(dict_len(author_last_set, authors['Last'][row]))
        num_shrt_last = float(dict_len(author_last_set, authors['Last'][row][:-1]))
        num_firsts = dict_len(author_first_set, authors['Firsts'][row]) 
	name_ratio = (num_long_name / num_shrt_name)
	last_ratio = (num_long_last / num_shrt_last)
	test_ratio = name_ratio * last_ratio
	if test_ratio <= 1:
	    test = num_long_name * np.sqrt(name_ratio) * np.sqrt(num_firsts) * num_long_last * np.sqrt(last_ratio)
	    if row in affs.index:
		for row2 in authors.index[authors['Name']==authors['Name'][row][:-1]]:
                    if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
			print "XXXXXXXXXX"
                        test = test / 100 
	    print num_long_name, num_shrt_name, num_long_last, num_shrt_last, num_firsts, "\t", int(test), "\t", authors['Name'][row],
            # a, b, c, x, y, and z seem to be extremely common end name bad characters
 	    if authors['Name'][row][:-1] in ['a','b','c','x','y','z','q','j']:
 		test = test / 2
	    if (test > 100):
                c2 += dict_len(author_set, authors['Name'][row])
	        print "XXXXXXXXXXXXXXXXXX TOO RISKY", c0, c1, c2
	    else:
                c0 += dict_len(author_set, authors['Name'][row])
                if author_set.__contains__(authors['Name'][row]):
                    auth_idx = author_set.pop(authors['Name'][row])
                    author_set[authors['Name'][row][:-1]] = auth_idx + author_set[authors['Name'][row][:-1]]
                    authors['Name'][auth_idx] = authors['Name'][row][:-1]
	        print 
	else:
	    test = num_shrt_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_firsts) * num_shrt_last * (1 / np.sqrt(last_ratio))
	    if row in affs.index:
		for row2 in authors.index[authors['Name']==authors['Name'][row][:-1]]:
                    if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
			print "XXXXXXXXXX"
                        test = test / 100
	    print num_long_name, num_shrt_name, num_long_last, num_shrt_last, num_firsts, "\t", int(test),  "\t", authors['Name'][row], "Flipped",
	    if (test > 50):
                c2 += dict_len(author_set, authors['Name'][row][:-1])
                print "XXXXXXXXXXXXXXXXXX TOO RISKY", c0, c1, c2
            else:
                c1 += dict_len(author_set, authors['Name'][row][:-1])
                auth_idx = author_set.pop(authors['Name'][row][:-1])
                author_set[authors['Name'][row]] = auth_idx + author_set[authors['Name'][row]]
                authors['Name'][auth_idx] = authors['Name'][row]
	        print 
####################################################################################
###################### i/y at end
####################################################################################
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names ending in i or y and seeing if they should be replaced
by the other letter"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
yi0,yi1,yi2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if authors['Name'][row][-1] == 'i' and authors['Name'][row][:-1] + "y" in author_set:
        num_old_name = float(dict_len(author_set, authors['Name'][row]))      # Higher is bad, ratio may matter more. Ratio may mean reverse
        num_new_name = float(dict_len(author_set, authors['Name'][row][:-1] + "y")) # Higher is good, ratio may matter more. Ratio may mean reverse
        num_old_last = float(dict_len(author_last_set, authors['Last'][row]))      # Higher is definately bad, ratio...not sure
        num_new_last = float(dict_len(author_last_set, authors['Last'][row][:-1] + "y")) # Higer is definately good, ratio...not sure
        num_firsts = dict_len(author_first_set, authors['Firsts'][row])       # Lower is definately good
        name_ratio = (num_old_name / num_new_name)
        last_ratio = (num_old_last / num_new_last)
        test_ratio = name_ratio * last_ratio
        if test_ratio <= 1:
            test = num_old_name * np.sqrt(name_ratio) * np.sqrt(num_firsts) * num_old_last * np.sqrt(last_ratio)
            print num_old_name, num_new_name, num_old_last, num_new_last, num_firsts, "\t", int(test), "\t", \
                authors['Name'][row], authors['Name'][row][:-1] + "y",
            if test > 50:
                yi2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY", yi0, yi1, yi2
            else:
                print
                yi0 += 1
                dict_move(author_set, authors['Name'][row], authors['Name'][row][:-1] + "y", row)
                authors['Name'][row] = authors['Name'][row][:-1] + "y"
        else:
            test = num_new_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_firsts) * num_new_last * (
                1 / np.sqrt(last_ratio))
            print num_old_name, num_new_name, num_old_last, num_new_last, num_firsts, "\t", int(test), "\t", \
                authors['Name'][row], authors['Name'][row][:-1] + "y", "Flipped",
            if test > 50:
                yi2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY", yi0, yi1, yi2
            else:
                yi1 += dict_len(author_set, authors['Name'][row][:-1] + "y")
                cur_idx = author_set[authors['Name'][row][:-1] + "y"]
                dict_move(author_set, authors['Name'][row][:-1] + "y", authors['Name'][row])
                authors['Name'][cur_idx] = authors['Name'][row]
                print
####################################################################################
###################### c/k at beginning 
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names beginning in c or k and seeing if they should be
replaced by the other letter"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
ck0,ck1,ck2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if authors['Name'][row][0] == 'k' and ("c" + authors['Name'][row][1:]) in author_set:
        num_old_name = float(dict_len(author_set, authors['Name'][row]))      # Higher is bad, ratio may matter more. Ratio may mean reverse
        num_new_name = float(dict_len(author_set, "c" + authors['Name'][row][1:])) # Higher is good, ratio may matter more. Ratio may mean reverse
        num_old_first = float(dict_len(author_first_set, authors['Firsts'][row]))      # Higher is definately bad, ratio...not sure
        num_new_first = float(dict_len(author_first_set, "c" + authors['Firsts'][row][1:])) # Higer is definately good, ratio...not sure
        num_last = dict_len(author_last_set, authors['Last'][row])       # Lower is definately good
        name_ratio = (num_old_name / num_new_name)
        first_ratio = (num_old_first / num_new_first)
        test_ratio = name_ratio * first_ratio
        if test_ratio <= 4:
            test = num_old_name * np.sqrt(name_ratio) * np.sqrt(num_last) * num_old_first * np.sqrt(first_ratio)
            print num_old_name, num_new_name, num_old_first, num_new_first, num_last, "\t", int(test), "\t", \
                authors['Name'][row], "c" + authors['Name'][row][1:],
            if test > 150:
                ck2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY", ck0, ck1, ck2
            else:
                print
                ck0 += 1
                dict_move(author_set, authors['Name'][row], "c" + authors['Name'][row][1:], row)
                authors['Name'][row] = ("c" + authors['Name'][row][1:])
        else:
            test = num_new_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_last) * num_new_first * (1 / np.sqrt(first_ratio))
            print num_old_name, num_new_name, num_old_first, num_new_first, num_last, "\t", int(test), "\t", \
                authors['Name'][row], "c" + authors['Name'][row][1:], "Flipped",
            if test > 150:
                ck2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY", ck0, ck1, ck2
            else:
                cur_idx = author_set[("c" + authors['Name'][row][1:])]
                ck1 += len(cur_idx)
                dict_move(author_set, ("c" + authors['Name'][row][1:]), authors['Name'][row])
                authors['Name'][cur_idx] = authors['Name'][row]
                print
####################################################################################
##################### "and" at end 
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names ending with a mistaken "and" """
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
and0,and1,and2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if authors['Name'][row][-3:] == 'and' and (authors['Name'][row][:-3]) in author_set:
        num_old_name = float(dict_len(author_set, authors['Name'][row]))      # Higher is bad, ratio may matter more. Ratio may mean reverse
        num_new_name = float(dict_len(author_set, authors['Name'][row][:-3])) # Higher is good, ratio may matter more. Ratio may mean reverse
        num_old_last = float(dict_len(author_last_set, authors['Last'][row]))      # Higher is definately bad, ratio...not sure
        num_new_last = float(dict_len(author_last_set, authors['Last'][row][:-3])) # Higer is definately good, ratio...not sure
        num_first = dict_len(author_first_set, authors['Firsts'][row])       # Lower is definately good
        name_ratio = (num_old_name / num_new_name)
        last_ratio = (num_old_last / num_new_last)
        test_ratio = name_ratio * last_ratio
        if test_ratio <= 4:
            test = num_old_name * np.sqrt(name_ratio) * np.sqrt(num_first) * num_old_last * np.sqrt(last_ratio)
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
                authors['Name'][row], authors['Name'][row][:-3],
            if test > 150:
                and2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
                print
                and0 += 1
                dict_move(author_set, authors['Name'][row], authors['Name'][row][:-3], row)
		authors['Name'][row] = (authors['Name'][row][:-3])
        else:
            test = num_new_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_first) * num_new_last * (1 / np.sqrt(last_ratio))
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
	    authors['Name'][row], authors['Name'][row][:-3], "Flipped",
            if test > 150:
                and2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
		cur_idx = author_set[(authors['Name'][row][:-3])]
                and1 += len(cur_idx)
		dict_move(author_set, (authors['Name'][row][:-3]), authors['Name'][row])
                authors['Name'][cur_idx] = authors['Name'][row]
                print
####################################################################################
##################### "yz" at end 
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names ending with a mistaken "yz" """
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
yz0,yz1,yz2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if authors['Name'][row][-2:] == 'yz' and (authors['Name'][row][:-2]) in author_set:
        num_old_name = float(dict_len(author_set, authors['Name'][row]))      # Higher is bad, ratio may matter more. Ratio may mean reverse
        num_new_name = float(dict_len(author_set, authors['Name'][row][:-2])) # Higher is good, ratio may matter more. Ratio may mean reverse
        num_old_last = float(dict_len(author_last_set, authors['Last'][row]))      # Higher is definately bad, ratio...not sure
        num_new_last = float(dict_len(author_last_set, authors['Last'][row][:-2])) # Higer is definately good, ratio...not sure
        num_first = dict_len(author_first_set, authors['Firsts'][row])       # Lower is definately good
        name_ratio = (num_old_name / num_new_name)
        last_ratio = (num_old_last / num_new_last)
        test_ratio = name_ratio * last_ratio
        if test_ratio <= 4:
            test = num_old_name * np.sqrt(name_ratio) * np.sqrt(num_first) * num_old_last * np.sqrt(last_ratio)
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
                authors['Name'][row], authors['Name'][row][:-2],
            if test > 150:
                yz2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
                print
                yz0 += 1
                dict_move(author_set, authors['Name'][row], authors['Name'][row][:-2], row)
		authors['Name'][row] = (authors['Name'][row][:-2])
        else:
            test = num_new_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_first) * num_new_last * (1 / np.sqrt(last_ratio))
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
	    authors['Name'][row], authors['Name'][row][:-2], "Flipped",
            if test > 150:
                yz2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
		cur_idx = author_set[(authors['Name'][row][:-2])]
                yz1 += len(cur_idx)
		dict_move(author_set, (authors['Name'][row][:-2]), authors['Name'][row])
                authors['Name'][cur_idx] = authors['Name'][row]
                print
print yz0,yz1,yz2
####################################################################################
##################### "ab" at end 
""" Refer back to backwards names, the logic of this block is very similar.  In this
case we are looking for names ending with a mistaken "ab" """
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join('.')
ab0,ab1,ab2=0,0,0
author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for row in authors.index:
    if authors['Name'][row][-2:] == 'ab' and (authors['Name'][row][:-2]) in author_set:
        num_old_name = float(dict_len(author_set, authors['Name'][row]))      # Higher is bad, ratio may matter more. Ratio may mean reverse
        num_new_name = float(dict_len(author_set, authors['Name'][row][:-2])) # Higher is good, ratio may matter more. Ratio may mean reverse
        num_old_last = float(dict_len(author_last_set, authors['Last'][row]))      # Higher is definately bad, ratio...not sure
        num_new_last = float(dict_len(author_last_set, authors['Last'][row][:-2])) # Higer is definately good, ratio...not sure
        num_first = dict_len(author_first_set, authors['Firsts'][row])       # Lower is definately good
        name_ratio = (num_old_name / num_new_name)
        last_ratio = (num_old_last / num_new_last)
        test_ratio = name_ratio * last_ratio
        if test_ratio <= 4:
            test = num_old_name * np.sqrt(name_ratio) * np.sqrt(num_first) * num_old_last * np.sqrt(last_ratio)
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
                authors['Name'][row], authors['Name'][row][:-2],
            if test > 150:
                ab2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
                print
                ab0 += 1
                dict_move(author_set, authors['Name'][row], authors['Name'][row][:-2], row)
		authors['Name'][row] = (authors['Name'][row][:-2])
        else:
            test = num_new_name * (1 / np.sqrt(name_ratio)) * np.sqrt(num_first) * num_new_last * (1 / np.sqrt(last_ratio))
            print num_old_name, num_new_name, num_old_last, num_new_last, num_first, "\t", int(test), "\t", \
	    authors['Name'][row], authors['Name'][row][:-2], "Flipped",
            if test > 150:
                ab2 += 1
                print "XXXXXXXXXXXXXXXXXX TOO RISKY"
            else:
		cur_idx = author_set[(authors['Name'][row][:-2])]
                ab1 += len(cur_idx)
		dict_move(author_set, (authors['Name'][row][:-2]), authors['Name'][row])
                authors['Name'][cur_idx] = authors['Name'][row]
                print
print ab0,ab1,ab2
####################################################################################
### Author Groups
""" Author groups are made from co-authors of duplicated papers.  Here we run through
each group and collect all the author names.  We then check each name against one 
another and test for similarity, as defined by the levenstein string distance. That's
then used as an input in a further test metrics (Refer back to backwards names)"""
ag = pd.read_csv("author_groups.csv")
ag['Name'] = ""
aid_grps = ag.groupby(['authorid'])
#################
for aid, group in aid_grps:
    if aid not in authors.index:
        print aid
        continue
    ag['Name'].ix[group.index] = authors['Name'][aid]
# cut names below certain length
ag = ag[:][ag['Name'].str.len()>8]
aids = sorted(set(ag['authorid'].values))
aid_grps = ag.groupby(['authorid'])
# lasts and firsts
ag0, ag1, ag2 = 0, 0, 0

author_set = authors.groupby(['Name']).groups
author_last_set = authors.groupby(['Last']).groups
author_first_set = authors.groupby(['Firsts']).groups
for aid, group in aid_grps:
    agroups = ag['authorgroup'].ix[group.index]
    coauthors = []
    for agrp in agroups: # agroups is a series of author groups tied to the author
	coauthors.extend(ag['Name'][ag['authorgroup']==agrp])
    coauthors = sorted(set(coauthors))
    name = authors['Name'][aid]
    names1 = name.split()
    for coa in coauthors:
	names2 = coa.split()
	if names1[0] == names2[0] and names1[-1] == names2[-1]:
	    continue
	lev = float(util.leven(ag['Name'][ag['authorid']==aid].values[0], coa))
	if lev < 5:
	    if lev >0:
		ag0 += 1
                num_n1 = float(dict_len(author_set, name))
                num_n2 = float(dict_len(author_set, coa))
                if num_n2 == 0:
                    continue
                # same last name
                if names1[-1] == names2[-1]:
                    num_last = float(dict_len(author_last_set, names1[-1]))
                    num_f1 = float(dict_len(author_first_set, ".".join(names1[:-1])))
                    num_f2 = float(dict_len(author_first_set, ".".join(names2[:-1])))
                    test_ratio = (float(len(".".join(names1[:-1]))) / float(len(".".join(names2[:-1])))) * (
                        num_n1 / num_n2) * (num_n1 / num_n2)
                    if test_ratio < 1: # changing to the 1st one, the ag one
                        if len(names2[0]) == 1 and names1[0][0] == names2[0][0]:
                            continue
                        else:
                            shorter = float(max(len(".".join(names1[:-1])), len(".".join(names2[:-1]))))
                            test = (lev / shorter) ** 6 * num_last * (num_n1 * num_n1 * num_n1) / num_n2
                            if test < 5:
                                if test < 0.071: #09
                                    ag1 += 1
                                    dict_move(author_set, authors['Name'][aid], coa, aid)
                                    authors['Name'][aid] = coa
				    if test > 0.01:
                                        print aid, lev, name, "|", coa
                                        print test, "\t", num_last, "|", int(num_n1), int(num_n2), "|", shorter, "\tsame last"
                                else:
                                    #print "\t\t\t", aid, lev, name, "|", coa
                                    #print "\t\t\t", test, "\t", num_last, "|", int(num_n1), int(num_n2), "|", shorter
                                    continue
                # same firsts
                elif names1[:-1] == names2[:-1]:
                    num_firsts = float(dict_len(author_first_set, ".".join(names1[:-1])))
                    num_l1 = float(float(dict_len(author_last_set, names1[-1])))
                    num_l2 = float(float(dict_len(author_last_set, names2[-1])))
                    test_ratio = (float(len(names2[-1])) / float(len(names1[-1]))) * (num_n1 / num_n2) * (
                        num_n1 / num_n2)
                    if test_ratio < 1: # changing to the 1st one, the ag one
                        shorter = float(max(len(names1[-1]), len(names2[-1])))
                        test = (lev / shorter) ** 6 * num_firsts * (num_n1 * num_n1 * num_n1) / num_n2
                        if test < 5:
                            if test < 0.30: # 09
                                ag2 += 1
                                dict_move(author_set, authors['Name'][aid], coa, aid)
                                authors['Name'][aid] = coa
				if test > 0.01:
                                    print aid, lev, name, "|", coa
                                    print test, "\t", num_firsts, "|", int(num_n1), int(num_n2), "|", shorter, "\tsame firsts"
                            else:
                                #print "\t\t\t", aid, lev, name, "|", coa
                                #print "\t\t\t", test, "\t", num_firsts, "|", int(num_n1), int(num_n2), "|", shorter
				continue
####################################################################################
####################################################################################
#### Names with Names
""" This ugle block of code looks for names that have extra words after or before
the "true" name.  For instance "Bill Gates Microsoft Research", or "Presented Ryan 
Seacrest"  I also look for names that should be extended, such as "Frank Lloyd" or
"James Earl" It's subdivided into blocks depending on the number of words in the 
name.  Within each block the logic is similar to reversed names above"""
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1]
authors['Firsts'] = authors['Firsts'].str.join(' ')
count3FL=0
count3FS=0
count3LS=0
count4FL=0
count4FS=0
count4LL=0
count4LS=0
count5FL=0
count5FS=0
count5LL1=0
count5LS1=0
count5LL2=0
count5LS2=0
names = set(authors['Name'].values)
for row in sorted(authors.index):
    if len(authors['Name'][row].split()) == 3:
	# Cut First Name
	if " ".join(authors['Name'][row].split()[1:]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[1:])
	    mid = authors['Name'][row].split()[1]
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_first = float(len(authors.index[authors['First']== authors['First'][row]]))
	    count_firsts = float(len(authors.index[authors['Firsts']== authors['Firsts'][row]]))
	    count_mid = float(len(authors.index[authors['First']== mid]))
	    count_last = float(len(authors.index[authors['Last']== authors['Last'][row]]))
	    name_ratio = (count_long / count_shrt)
	    firsts_ratio = (count_firsts / count_mid)
	    test_ratio = name_ratio * name_ratio * firsts_ratio * count_firsts 
	    if test_ratio >= 1: # make it the longer name
		test =  count_last * count_shrt * count_shrt * count_shrt * count_mid * count_mid * count_mid / (count_first * count_firsts * count_long)
		if row in affs.index:
		    for row2 in authors.index[authors['Name']==long_name]:
                        if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
		            print row, row2, "XXXXXXXXXXXXXXXX"
                            test = test / 100
		if test < 25:
		    count3FL += 1
                    authors['Name'][authors['Name']==shrt_name] = long_name
                    names = set(authors['Name'].values)
                    print "A", row, int(test), "|", count_last, "|", count_long, count_shrt, "|", count_first, count_firsts, count_mid, shrt_name, "\t\t", long_name
	    else:
		test =  count_last * count_long * count_long * count_long * count_first * count_mid * count_firsts / (count_shrt * count_shrt)
		if row in affs.index:
		    for row2 in authors.index[authors['Name']==shrt_name]:
                        if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
		            print row, row2, "XXXXXXXXXXXXXXXX"
                            test = test / 100
		if test < 250:
		    count3FS += 1
                    authors['Name'][row] = shrt_name
                    names = set(authors['Name'].values)
                    print "B", row, int(test), "|", count_last, "|", count_long, count_shrt, "|", count_first, count_firsts, count_mid, long_name, "\t\t", shrt_name
	# cut last name
	elif " ".join(authors['Name'][row].split()[:2]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[:2])
	    mid = authors['Name'][row].split()[1]
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_first = float(len(authors.index[authors['First']== authors['First'][row]]))
	    count_firsts = float(len(authors.index[authors['Firsts']== authors['Firsts'][row]]))
	    count_last = float(len(authors.index[authors['Last']== authors['Last'][row]]))
	    count_mid = float(len(authors.index[authors['Last']== mid]))
	    name_ratio = (count_long / count_shrt)
	    last_ratio = (count_last / count_mid)
	    test_ratio = name_ratio * name_ratio * last_ratio * count_last
	    # to 4th power? (long, last?) or 1st - mid/short
            test =  count_first * count_long * count_long * count_long * count_last * count_last * count_last * count_firsts / (count_shrt * count_shrt)
	    if row in affs.index:
	        for row2 in authors.index[authors['Name']==shrt_name]:
                    if row2 in affs.index and util.check_affs(affs['Affiliation'][row], affs['Affiliation'][row2]):
		        print row, row2, "XXXXXXXXXXXXXXXX"
                        test = test / 100
	    if test < 100:
	        count3LS += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
                print "C", row, int(test), "|", count_firsts, count_first, "|", count_long, count_shrt, "|", count_last, count_mid, long_name, "\t\t", shrt_name
    elif len(authors['Name'][row].split()) == 4:
	# Cut First Name
	if " ".join(authors['Name'][row].split()[1:]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[1:])
	    new_firsts = " ".join(authors['Name'][row].split()[1:-1])
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_cut = float(len(authors.index[authors['Firsts']== authors['Firsts'][row]]))
	    count_new = float(len(authors.index[authors['Firsts']== new_firsts]))
	    name_ratio = (count_long / count_shrt)
	    firsts_ratio = (count_cut / count_new)
	    test_ratio = name_ratio * name_ratio * firsts_ratio
	    if test_ratio >= 1: # make it the longer name
		count4FL += 1
                authors['Name'][authors['Name']==shrt_name] = long_name
                names = set(authors['Name'].values)
	    else:
		count4FS += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
	# cut last name
	elif " ".join(authors['Name'][row].split()[:3]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[:3])
	    new_last = " ".join(authors['Name'][row].split()[2:3])
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_cut = float(len(authors.index[authors['Last']== authors['Last'][row]]))
	    count_new = float(len(authors.index[authors['Last']== new_last]))
	    name_ratio = (count_long / count_shrt)
	    last_ratio = (count_cut / count_new)
	    test_ratio = name_ratio * name_ratio * last_ratio
	    if test_ratio >= 1: # make it the longer name
		count4LL += 1
                authors['Name'][authors['Name']==shrt_name] = long_name
                names = set(authors['Name'].values)
	    else:
		count4LS += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
    # cut last names
    elif len(authors['Name'][row].split()) > 4:
	if " ".join(authors['Name'][row].split()[:4]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[:4])
	    new_last = " ".join(authors['Name'][row].split()[3:4])
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_cut = float(len(authors.index[authors['Last']== authors['Last'][row]]))
	    count_new = float(len(authors.index[authors['Last']== new_last]))
	    name_ratio = (count_long / count_shrt)
	    last_ratio = (count_cut / count_new)
	    test_ratio = name_ratio * name_ratio * last_ratio
	    if test_ratio >= 1: # make it the longer name
		count5LL1 += 1
                authors['Name'][authors['Name']==shrt_name] = long_name
                names = set(authors['Name'].values)
	    else:
		count5LS1 += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
	elif " ".join(authors['Name'][row].split()[:3]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[:3])
	    new_last = " ".join(authors['Name'][row].split()[2:3])
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_cut = float(len(authors.index[authors['Last']== authors['Last'][row]]))
	    count_new = float(len(authors.index[authors['Last']== new_last]))
	    name_ratio = (count_long / count_shrt)
	    last_ratio = (count_cut / count_new)
	    test_ratio = name_ratio * name_ratio * last_ratio
	    if test_ratio >= 1: # make it the longer name
		count5LL2 += 1
                authors['Name'][authors['Name']==shrt_name] = long_name
                names = set(authors['Name'].values)
	    else:
		count5LS2 += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
	elif " ".join(authors['Name'][row].split()[1:]) in names:
	    long_name = authors['Name'][row]
	    shrt_name = " ".join(authors['Name'][row].split()[1:])
	    new_firsts = " ".join(authors['Name'][row].split()[1:-1])
	    count_long = float(len(authors.index[authors['Name']==long_name]))
	    count_shrt = float(len(authors.index[authors['Name']==shrt_name]))
	    count_cut = float(len(authors.index[authors['Firsts']== authors['Firsts'][row]]))
	    count_new = float(len(authors.index[authors['Firsts']== new_firsts]))
	    name_ratio = (count_long / count_shrt)
	    firsts_ratio = (count_cut / count_new)
	    test_ratio = name_ratio * name_ratio * firsts_ratio
	    if test_ratio >= 1: # make it the longer name
		count5FL += 1
                authors['Name'][authors['Name']==shrt_name] = long_name
                names = set(authors['Name'].values)
	    else:
		count5FS += 1
                authors['Name'][row] = shrt_name
                names = set(authors['Name'].values)
####################################################################################
####################################################################################
### Grab the various components of each name
authors['Last'] = authors['Name'].str.split().str[-1]
authors['Firsts'] = authors['Name'].str.split().str[:-1] # First and Middle and everything except last name
authors['Firsts'] = authors['Firsts'].str.join('.')
authors['First'] = authors['Name'].str.split().str[0]    # First name only
authors['FI'] = authors['First'].str[0]    # First Initial
authors['Mids'] = authors['Firsts'].str.split(".").str[1:] # Everything except first and last name
authors['Mids'] = authors['Mids'].str.join('.')
authors['Mids'] = authors['Mids'].str.replace("nan", "nahn")
####################################################################################
####################################################################################
# The "Nick" value holds short names like Ben, Chris, etc..and names which could 
# easily be mistaken for one another.  Later on I group names by first initial, last
# name.  That is why in cases where the nickname begins with a different character I
# also change the first name (Anthony and Tony, for instance).
authors['Nick'] = authors['First']
authors['Nick'][authors['First']=='agnes'] = 'agi'
authors['Nick'][authors['First']=='abraham'] = 'abe'
authors['Nick'][authors['First']=='avi'] = 'abe'
authors['Nick'][authors['First']=='albert'] = 'al'
authors['Nick'][authors['First']=='alexander'] = 'alex'
authors['Nick'][authors['First']=='alek'] = 'alex' ##
authors['Nick'][authors['First']=='aleksandar'] = 'alex' ##
authors['Nick'][authors['First']=='aleksander'] = 'alex' ##
authors['Nick'][authors['First']=='aleksandr'] = 'alex' ##
authors['Nick'][authors['First']=='aleksandra'] = 'alex' ##
authors['Nick'][authors['First']=='alexandr'] = 'alex' ##
authors['Nick'][authors['First']=='alexandra'] = 'alex' ##
authors['Nick'][authors['First']=='alexandre'] = 'alex' ##
authors['Nick'][authors['First']=='alexandros'] = 'alex' ##
authors['Nick'][authors['First']=='alexandru'] = 'alex' ##
authors['Nick'][authors['First']=='alexei'] = 'alex' ##
authors['Nick'][authors['First']=='alexey'] = 'alex' ##
authors['Nick'][authors['First']=='alexis'] = 'alex' ##
authors['Nick'][authors['First']=='alen'] = 'alan' ##
authors['Nick'][authors['First']=='allen'] = 'alan' ##
authors['Nick'][authors['First']=='allan'] = 'alan' ##
authors['Nick'][authors['First']=='alan'] = 'alan' ##   # al?
authors['Nick'][authors['First']=='alfons'] = 'alphons' ##   # al?
authors['Nick'][authors['First']=='fons'] = 'alphons' ##   # al?
authors['First'][authors['First']=='fons'] = 'aplhonsxxxx'
authors['Nick'][authors['First']=='alhons'] = 'alphons' ##   # al?
authors['Nick'][authors['First']=='andrew'] = 'andy'
authors['Nick'][authors['First']=='andre'] = 'andre' ##   # al?
authors['Nick'][authors['First']=='andreas'] = 'andre' ##   # al?
authors['Nick'][authors['First']=='andrei'] = 'andre' ##   # al?
authors['Nick'][authors['First']=='arthur'] = 'art'
authors['Nick'][authors['First']=='artur'] = 'art'
authors['Nick'][authors['First']=='arturs'] = 'art'
authors['Nick'][authors['First']=='arturo'] = 'art'
authors['Nick'][authors['First']=='bartholomew'] = 'bart'
authors['Nick'][authors['First']=='benjamin'] = 'ben'
authors['Nick'][authors['First']=='bernard'] = 'bernie'
authors['Nick'][authors['First']=='bertrand'] = 'bert'
authors['Nick'][authors['First']=='bobby'] = 'rob'
authors['First'][authors['First']=='bobby'] = 'robbxzy'
authors['Nick'][authors['First']=='brian'] = 'brian' ##   # al?
authors['Nick'][authors['First']=='bryan'] = 'brian' ##   # al?
authors['Nick'][authors['First']=='chadwick'] = 'chad'
authors['Nick'][authors['First']=='charles'] = 'chuck'
authors['Nick'][authors['First']=='ch'] = 'chuck'
authors['Nick'][authors['First']=='chester'] = 'chet'
authors['Nick'][authors['First']=='christopher'] = 'chris'
authors['Nick'][authors['First']=='christian'] = 'chris' #
authors['Nick'][authors['First']=='christoph'] = 'chris' #
authors['Nick'][authors['First']=='christophe'] = 'chris' #
authors['Nick'][authors['First']=='clifford'] = 'cliff'
authors['Nick'][authors['First']=='cornelus'] = 'cornelius'
authors['Nick'][authors['First']=='cornelis'] = 'cornelius'
authors['Nick'][authors['First']=='cees'] = 'cornelius'
authors['Nick'][authors['First']=='csaba'] = 'cs'
authors['Nick'][authors['First']=='curtis'] = 'curt'
authors['Nick'][authors['First']=='david'] = 'dave'
authors['Nick'][authors['First']=='dick'] = 'rick'
authors['First'][authors['First']=='dick'] = 'ricszzzz'
authors['Nick'][authors['First']=='daniel'] = 'dan'
authors['Nick'][authors['First']=='danny'] = 'dan'
authors['Nick'][authors['First']=='dennis'] = 'denis'
authors['Nick'][authors['First']=='dimitri'] = 'dmitry'
authors['Nick'][authors['First']=='dmitri'] = 'dmitry'
authors['Nick'][authors['First']=='dimitrios'] = 'dmitry'
authors['Nick'][authors['First']=='dimitris'] = 'dmitry'
authors['Nick'][authors['First']=='dominic'] = 'dom'
authors['Nick'][authors['First']=='dominick'] = 'dom'
authors['Nick'][authors['First']=='dominik'] = 'dom'  #####
authors['Nick'][authors['First']=='donald'] = 'don'
authors['Nick'][authors['First']=='douglas'] = 'doug'
authors['Nick'][authors['First']=='edgar'] = 'ed'
authors['Nick'][authors['First']=='edward'] = 'ed'
authors['Nick'][authors['First']=='edwin'] = 'ed'
authors['Nick'][authors['First']=='eduardo'] = 'ed'
authors['Nick'][authors['First']=='eddie'] = 'ed'
authors['Nick'][authors['First']=='eddy'] = 'ed'
authors['Nick'][authors['First']=='eric'] = 'erik' ##
authors['Nick'][authors['First']=='francoise'] = 'francois'   ##
authors['Nick'][authors['First']=='frances'] = 'frank'
authors['Nick'][authors['First']=='francis'] = 'frank'   ##
authors['Nick'][authors['First']=='francisco'] = 'frank' ##
authors['Nick'][authors['First']=='fredrick'] = 'fred' ##
authors['Nick'][authors['First']=='fredrik'] = 'fred' ##
authors['Nick'][authors['First']=='frdric'] = 'fred' ##
authors['Nick'][authors['First']=='frdrik'] = 'fred' ##
authors['Nick'][authors['First']=='frdrick'] = 'fred' ##
authors['Nick'][authors['First']=='fredrik'] = 'fred' ##
authors['Nick'][authors['First']=='frederick'] = 'fred'
authors['Nick'][authors['First']=='frederic'] = 'fred'
authors['Nick'][authors['First']=='fredy'] = 'fred'
authors['Nick'][authors['First']=='geoffrey'] = 'geoff'
authors['Nick'][authors['First']=='giorgos'] = 'george'
authors['Nick'][authors['First']=='georgii'] = 'george'
authors['Nick'][authors['First']=='georgy'] = 'george'
authors['Nick'][authors['First']=='gregory'] = 'greg'
authors['Nick'][authors['First']=='gregg'] = 'greg' #######################
authors['Nick'][authors['First']=='gregor'] = 'greg' #######################
authors['Nick'][authors['First']=='gregorio'] = 'greg' #######################
authors['Nick'][authors['First']=='freddy'] = 'fred'
authors['Nick'][authors['First']=='henry'] = 'hank'
authors['Nick'][authors['First']=='henri'] = 'hank' ##############################
authors['Nick'][authors['First']=='herbert'] = 'herb'
authors['Nick'][authors['First']=='herber'] = 'herb'
authors['Nick'][authors['First']=='irving'] = 'irv'
authors['Nick'][authors['First']=='jacob'] = 'jake'
authors['Nick'][authors['First']=='james'] = 'jim'
authors['Nick'][authors['First']=='jimmy'] = 'jim'
authors['Nick'][authors['First']=='jimmie'] = 'jim'
authors['Nick'][authors['First']=='jeffrey'] = 'jeff'
authors['Nick'][authors['First']=='jofish'] = 'josephjofish'
authors['Nick'][authors['First']=='joseph'] = 'joe'
authors['Nick'][authors['First']=='josef'] = 'joe'
authors['Nick'][authors['First']=='josep'] = 'joe'
authors['Nick'][authors['First']=='joey'] = 'joe'
authors['Nick'][authors['First']=='john'] = 'jack'
authors['Nick'][authors['First']=='johnathon'] = 'jack' ###
authors['Nick'][authors['First']=='jonathon'] = 'jack' ###
authors['Nick'][authors['First']=='jon'] = 'jack' ###
authors['Nick'][authors['First']=='joshua'] = 'josh'
authors['Nick'][authors['First']=='kenneth'] = 'ken'
authors['Nick'][authors['First']=='kenny'] = 'ken'
authors['Nick'][authors['First']=='kurtis'] = 'kurt'
authors['Nick'][authors['First']=='lawrence'] = 'larry'
authors['Nick'][authors['First']=='laurence'] = 'larry'
authors['Nick'][authors['First']=='leonard'] = 'leo'
authors['Nick'][authors['First']=='leonid'] = 'leo'
authors['Nick'][authors['First']=='leonel'] = 'leo'
authors['Nick'][authors['First']=='leonardo'] = 'leo'
authors['Nick'][authors['First']=='louis'] = 'lou'
authors['Nick'][authors['First']=='louise'] = 'lou'
authors['Nick'][authors['First']=='luis'] = 'lou'
authors['Nick'][authors['First']=='luise'] = 'lou'
authors['Nick'][authors['First']=='luiz'] = 'lou'
authors['Nick'][authors['First']=='lucas'] = 'luke'
authors['Nick'][authors['First']=='lukas'] = 'luke'
authors['Nick'][authors['First']=='lukasz'] = 'luke'
authors['Nick'][authors['First']=='luc'] = 'luke'
authors['Nick'][authors['First']=='luca'] = 'luke'
authors['Nick'][authors['First']=='manuel'] = 'manny'
authors['Nick'][authors['First']=='marc'] = 'mark' ###
authors['Nick'][authors['First']=='mark'] = 'mark' ###
authors['Nick'][authors['First']=='marcus'] = 'mark' ###
authors['Nick'][authors['First']=='markus'] = 'mark' ###
authors['Nick'][authors['First']=='matthias'] = 'matt'
authors['Nick'][authors['First']=='matthew'] = 'matt'
authors['Nick'][authors['First']=='marvin'] = 'marv'
authors['Nick'][authors['First']=='maximillian'] = 'max'
authors['Nick'][authors['First']=='maxwell'] = 'max'
authors['Nick'][authors['First']=='michael'] = 'mike'
authors['Nick'][authors['First']=='mitchell'] = 'mitch'
authors['Nick'][authors['First']=='mitchel'] = 'mitch'
authors['Nick'][authors['First']=='mohamed'] = 'mohamed' #
authors['Nick'][authors['First']=='mohammad'] = 'mohamed' #
authors['Nick'][authors['First']=='nathan'] = 'nate'
authors['Nick'][authors['First']=='nathaniel'] = 'nate'
authors['Nick'][authors['First']=='nicolas'] = 'nico'
authors['Nick'][authors['First']=='nicholas'] = 'nick'
authors['Nick'][authors['First']=='nic'] = 'nick' ##
authors['Nick'][authors['First']=='normand'] = 'norm'
authors['Nick'][authors['First']=='panayotis'] = 'panayiotis'
authors['Nick'][authors['First']=='patrick'] = 'pat'
authors['Nick'][authors['First']=='patrik'] = 'pat'
authors['Nick'][authors['First']=='peter'] = 'pete'
authors['Nick'][authors['First']=='pieter'] = 'pete'
authors['Nick'][authors['First']=='petr'] = 'pete'      ###
authors['Nick'][authors['First']=='phillip'] = 'phil'
authors['Nick'][authors['First']=='phillipe'] = 'phil'
authors['Nick'][authors['First']=='phillipp'] = 'phil'
authors['Nick'][authors['First']=='phillippe'] = 'phil'
authors['Nick'][authors['First']=='philip'] = 'phil'
authors['Nick'][authors['First']=='philipe'] = 'phil'
authors['Nick'][authors['First']=='philipp'] = 'phil'
authors['Nick'][authors['First']=='philippe'] = 'phil'
authors['Nick'][authors['First']=='ph'] = 'phil'
authors['Nick'][authors['First']=='ralf'] = 'ralph' ##
authors['Nick'][authors['First']=='randolph'] = 'randy'
authors['Nick'][authors['First']=='rafael'] = 'rafi'
authors['Nick'][authors['First']=='rafaele'] = 'rafi'
authors['Nick'][authors['First']=='raphael'] = 'rafi'
authors['Nick'][authors['First']=='rajeev'] = 'raf'
authors['Nick'][authors['First']=='rajev'] = 'raf'
authors['Nick'][authors['First']=='rajiv'] = 'raf'
authors['Nick'][authors['First']=='randolph'] = 'rafi'
authors['Nick'][authors['First']=='randolph'] = 'rafi'
authors['Nick'][authors['First']=='raymond'] = 'ray'
authors['Nick'][authors['First']=='rich'] = 'rick'
authors['Nick'][authors['First']=='richard'] = 'rick'
authors['Nick'][authors['First']=='ricardo'] = 'rick'
authors['Nick'][authors['First']=='robby'] = 'rob'
authors['Nick'][authors['First']=='robert'] = 'rob'
authors['Nick'][authors['First']=='roberto'] = 'rob'
authors['Nick'][authors['First']=='rodney'] = 'rod'
authors['Nick'][authors['First']=='ronald'] = 'ron'
authors['Nick'][authors['First']=='russell'] = 'russ'
authors['Nick'][authors['First']=='sandra'] = 'sandy'
authors['Nick'][authors['First']=='shahram'] = 'sh'
authors['Nick'][authors['First']=='shawn'] = 'shaun'  ##
authors['Nick'][authors['First']=='shavkat'] = 'sh'
authors['Nick'][authors['First']=='stanley'] = 'stan'
authors['Nick'][authors['First']=='stephen'] = 'steve' #
authors['Nick'][authors['First']=='steven'] = 'steve'
authors['Nick'][authors['First']=='samuel'] = 'sam'
authors['Nick'][authors['First']=='sidney'] = 'sid'
authors['Nick'][authors['First']=='terrance'] = 'terry'  ###
authors['Nick'][authors['First']=='terrence'] = 'terry'
authors['Nick'][authors['First']=='terence'] = 'terry' #
authors['Nick'][authors['First']=='terri'] = 'terry'     ###
authors['Nick'][authors['First']=='theodore'] = 'ted'
authors['Nick'][authors['First']=='theo'] = 'ted'
authors['Nick'][authors['First']=='toby'] = 'tobias' #
authors['Nick'][authors['First']=='tobi'] = 'tobias' #
authors['Nick'][authors['First']=='thomas'] = 'tom'
authors['Nick'][authors['First']=='tomas'] = 'tom' #
authors['Nick'][authors['First']=='th'] = 'tom'
authors['Nick'][authors['First']=='timothy'] = 'tim'
authors['Nick'][authors['First']=='tony'] = 'anthony'
authors['First'][authors['First']=='tony'] = 'anthonyxyz'
authors['Nick'][authors['First']=='victor'] = 'vic'
authors['Nick'][authors['First']=='viktor'] = 'vic'
authors['Nick'][authors['First']=='vincent'] = 'vince'
authors['Nick'][authors['First']=='vincenzo'] = 'vince'
authors['Nick'][authors['First']=='vladimir'] = 'vlad'
authors['Nick'][authors['First']=='walter'] = 'walt'
authors['Nick'][authors['First']=='william'] = 'will'
authors['Nick'][authors['First']=='will'] = 'will'
authors['Nick'][authors['First']=='wilfred'] = 'will'
authors['Nick'][authors['First']=='wolfram'] = 'wolf'
authors['Nick'][authors['First']=='yuri'] = 'yury'
authors['Nick'][authors['First']=='bill'] = 'will'
authors['First'][authors['First']=='bill'] = 'willbxz'
authors['Nick'][authors['First']=='aimee'] = 'amy'
authors['Nick'][authors['First']=='ana'] = 'anna'
authors['Nick'][authors['First']=='ann'] = 'anna'
authors['Nick'][authors['First']=='anne'] = 'anna'
authors['Nick'][authors['First']=='annette'] = 'anna'
authors['Nick'][authors['First']=='catherine'] = 'cathy'
authors['Nick'][authors['First']=='christine'] = 'chrissy'
authors['Nick'][authors['First']=='clare'] = 'clair'
authors['Nick'][authors['First']=='cynthia'] = 'cyndy'
authors['Nick'][authors['First']=='deborah'] = 'debbie'
authors['Nick'][authors['First']=='debra'] = 'debbie'
authors['Nick'][authors['First']=='helen'] = 'helene'
authors['Nick'][authors['First']=='jennifer'] = 'jen'
authors['Nick'][authors['First']=='jenifer'] = 'jen'
authors['Nick'][authors['First']=='liz'] = 'elizabeth'
authors['First'][authors['First']=='liz'] = 'elizabethsdsf'
authors['Nick'][authors['First']=='florence'] = 'flo'
authors['Nick'][authors['First']=='frances'] = 'fran'
authors['Nick'][authors['First']=='janet'] = 'jan'
authors['Nick'][authors['First']=='janett'] = 'jan'
authors['Nick'][authors['First']=='juliana'] = 'julie'
authors['Nick'][authors['First']=='julia'] = 'julie'
authors['Nick'][authors['First']=='katherine'] = 'kathy'
authors['Nick'][authors['First']=='kathleen'] = 'kathy'
authors['Nick'][authors['First']=='kimberly'] = 'kim'
authors['Nick'][authors['First']=='janice'] = 'jan'
authors['Nick'][authors['First']=='margaret'] = 'marge'
authors['Nick'][authors['First']=='natalya'] = 'natalia'
authors['Nick'][authors['First']=='nouredine'] = 'nordine'
authors['Nick'][authors['First']=='pamela'] = 'pam'
authors['Nick'][authors['First']=='sarah'] = 'sally'
authors['Nick'][authors['First']=='sara'] = 'sally'
authors['Nick'][authors['First']=='sophia'] = 'sophie'
authors['Nick'][authors['First']=='susan'] = 'sue'
authors['Nick'][authors['First']=='susanne'] = 'sue'
authors['Nick'][authors['First']=='susan'] = 'sue'
authors['Nick'][authors['First']=='susana'] = 'sue'
authors['Nick'][authors['First']=='susanna'] = 'sue'
authors['Nick'][authors['First']=='suzanne'] = 'sue'
authors['Nick'][authors['First']=='suzan'] = 'sue'
authors['Nick'][authors['First']=='suzana'] = 'sue'
authors['Nick'][authors['First']=='teresa'] = 'terry'
authors['Nick'][authors['First']=='valerie'] = 'val'
authors['Nick'][authors['First']=='valery'] = 'val'
authors['Nick'][authors['First']=='victoria'] = 'vicky'
authors['Nick'][authors['First']=='vickie'] = 'vicky'
authors['Nicks'] = authors['Nick'] + authors['Mids']
authors['FI'] = authors['First'].str[0]    # First Initial
###############################################################################
################ Count frequency of first and last names. Runtime..about 5 hrs
###############################################################################
# Count frequency of last names
authors['last_freq'] = 0
lasts = authors.groupby(['Last']).groups
for name in lasts.keys():
    count = len(lasts[name])
    if count > 999:
        print count, name # print the most common names
    authors['last_freq'].ix[lasts[name]] = count
# Count frequency of "firsts" names (all of a name that is not the last name. George H W for example)
authors['firsts_freq'] = 0
firstss = authors.groupby(['Firsts']).groups
for name in firstss.keys():
    count = len(firstss[name])
    authors['firsts_freq'].ix[firstss[name]] = count
# Count frequency of first names
authors['first_freq'] = 0
firsts = authors.groupby(['First']).groups
for name in firsts.keys():
    count = len(firsts[name])
    if count > 999:
        print count, name # print the most common names
    authors['first_freq'].ix[firsts[name]] = count
# Count frequency of First Initials
authors['fi_freq'] = 0
fis = authors.groupby(['FI']).groups
for name in fis.keys():
    count = len(fis[name])
    authors['fi_freq'].ix[fis[name]] = count
# Count frequency of nick Names
authors['nick_freq'] = 0
nick = authors.groupby(['Nick']).groups
for name in nick.keys():
    count = len(nick[name])
    authors['nick_freq'].ix[nick[name]] = count
# Count frequency of nick Names
authors['nicks_freq'] = 0
nicks = authors.groupby(['Nicks']).groups
for name in nicks.keys():
    count = len(nicks[name])
    if count > 999:
        print count, name # print the most common names
    authors['nicks_freq'].ix[nicks[name]] = count
authors.to_csv('freq54.csv') # store for later
