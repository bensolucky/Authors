"""
This code reads in the afiiliations column from Author.csv.  It parses out
non-alphabetic characters, space-seperates the values and then remvoves some
of the most common/generic words.  Later we use the remaining 
commmon-affiliation terms to determine that authors are true duplicates.
"""
import pandas as pd
import sys
authors = pd.read_csv("Author.csv", index_col=0)
affs = pd.DataFrame(authors['Affiliation'])
affs['Affiliation'] = affs['Affiliation'].str.rstrip()
affs['Affiliation'] = affs['Affiliation'].str.lstrip()
affs['Affiliation'] = affs['Affiliation'].str.lower()

# Foreign Language Special Characters
affs['Affiliation'] = affs['Affiliation'].str.replace("\xe2\x80\x99", "'") #84 apostrophe
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc2\xa8\xc2\xa2", "a") #32 Spanish a
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc2\xa8", "") # 445 next character is an umlatts
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa8", "e") # 19 French e
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xad", "i") # 73 Spanish i
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa4", "a") # 66 German a
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xaa", "e") # 2 Portugese E
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa3", "a") # 17 Portugese A
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb3", "o") # 55 Portugese O
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb6", "0") # 127 Swedish O
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\x96", "o") # 13 Swedish o
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xaf", "i") # 3 Catalonian I
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb8", "o") # 20 Icelandic O
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xba", "u") # 18 Catalonian u
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\x85", "a") # 2 Norwegian A
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\x89", "e") # 6 Swiss e
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa9", "e") # 234 French e
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\x9c", "u") # 5 Turkish U
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xbc", "u") # 109 German u
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb1", "n") # 22 Spanish N
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb4", "o") # 3 French O
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa1", "a") # 105 Hungarian a
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa7", "c") # 28 Portugese c
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\x9f", "b") # 15 German B
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb5", "o") # 16 Portugese o
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa5", "a") # 4 Some? a
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xa0", "a") # 3 Some? a
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xab", "e") # 4 Some? e
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc3\xb2", "o") # 1 Some? o
affs['Affiliation'] = affs['Affiliation'].str.replace("\xc5\x81", "l") # 4 Slavic L
# Remove some non-alphanumerics
affs['Affiliation'] = affs['Affiliation'].str.replace('|',' ')
affs['Affiliation'] = affs['Affiliation'].str.replace(',',' ')
affs['Affiliation'] = affs['Affiliation'].str.replace('\"','')
affs['Affiliation'] = affs['Affiliation'].str.replace('\'','')
affs['Affiliation'] = affs['Affiliation'].str.replace('(','')
affs['Affiliation'] = affs['Affiliation'].str.replace(')','')
affs['Affiliation'] = affs['Affiliation'].str.replace('.','')
affs['Affiliation'] = affs['Affiliation'].str.replace(';','')
affs['Affiliation'] = affs['Affiliation'].str.replace('-',' ')
affs['Affiliation'] = affs['Affiliation'].str.replace('&','')
# Now get rid of some generic/common terms in serveral languages
affs['Affiliation'] = affs['Affiliation'].str.replace(' inc','')
for word in [' for ',' fur ',' et ',' a ',' and ',' und ',' y ',' at ',' in ',' of ',' von ',' des ',' de ',' di ',' 1 ']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,' ')
for word in ['^the ', '^las ','^la ','^il ','^el ','^los ','^der ']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,'')
for word in [' the ', ' las ',' la ',' il ',' el ',' los ',' der ']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,' ')
for word in ['institute','institut','science','research','center','national','nacional']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,'')
for word in ['department', 'dept', 'departamento', 'dipartimento', 'university', 'universidad', 'universitat', 'universiteit', 'technische', 'technology', 'laboratory']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,'')
for word in ['corporation', 'usa', 'school', 'college', 'state', 'group','division', 'faculty', 'faculdad']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,'')
for word in ['universidade', 'faculdade', 'federal', 'depto']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,'')
for word in [' new ', ' st ']:
    affs['Affiliation'] = affs['Affiliation'].str.replace(word,' ')
# Get rid of single character "words"
affs['Affiliation'] = affs['Affiliation'].str.replace('^[0-9] ','')
affs['Affiliation'] = affs['Affiliation'].str.replace(' [0-9] ',' ')
affs['Affiliation'] = affs['Affiliation'].str.replace('^[a-z] ','')
affs['Affiliation'] = affs['Affiliation'].str.replace(' [a-z] ',' ')

affs['Affiliation'] = affs['Affiliation'].str.rstrip()
affs['Affiliation'] = affs['Affiliation'].str.lstrip()

# Remove rows where affiliations is now empty
print len(affs.index)
affs = affs[:][pd.notnull(affs['Affiliation'])]
print len(affs.index)
affs = affs[:][affs['Affiliation']!='']
print len(affs.index)
affs = affs[:][affs['Affiliation']!=' ']
print len(affs.index)
print affs.head()
print affs.tail()
# space-seperate the values and print them to a file.
""" I'm sure there's a better way to print list-valued rows in pandas, but I
haven't had time to figure that out, instead I'm just using this "tab 
seperated value" format, and a reader for this type of file in my utils.py """
affs['Affiliation'] = affs['Affiliation'].str.split()
affs['Affiliation'].to_csv('affs_loose.tsv', sep='\t', header=['Affiliation'])

"""
The below commented-out piece of code was used to find the most common words 
in the affiliations column.  Those words were then mostly deleted in the code 
above.
"""
#words=[]
#for id in affs.index:
#    words.extend(affs['Affiliation'][id])
#bad_words = []
#for word in words:
#    print words.count(word), word
#    if words.count(word) > 1000 and word not in bad_words:
#	bad_words.append(word)
#	bad_words.append(words.count(word))
#print bad_words
