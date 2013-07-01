import pandas as pd
import numpy as np
import time

start_time = time.time()

""" Either Dmitry or Lucas wrote this.  It finds "duplicate papers" and creates 
groupings of all authors who have authored these papers.  The idea is that 2 papers
with the same title are likely the same paper, somehow duplicated within the MAS
database.  An author may have his/her name spelled differently in the various 
duplicated paper records.  These various spellings can be used to identify
duplicates"""
####################################################################################
# load data
####################################################################################
authors = pd.read_csv("Author.csv")
papers = pd.read_csv("Paper.csv")
author_papers = pd.read_csv("PaperAuthor.csv")

####################################################################################
# remove author paper duplicates and not in author set
####################################################################################
author_papers = author_papers[['AuthorId', 'PaperId']]
author_papers = author_papers.drop_duplicates()
author_papers = author_papers[:][author_papers.AuthorId.isin(authors.Id)]

author_papers = author_papers.sort(['AuthorId', 'PaperId'])

####################################################################################
# clean paper title
####################################################################################
papers = papers.drop(['Year', 'ConferenceId', 'JournalId', 'Keyword'], axis=1)
papers.Title = papers.Title.str.lower()
papers.Title = papers.Title.str.replace("[^a-z0-9]", " ")
papers.Title = papers.Title.str.replace("\\s+", " ")
papers.Title = papers.Title.str.strip()
papers = papers[:][papers.Id.isin(author_papers.PaperId)]
papers = papers[:][pd.notnull(papers.Title)]
papers = papers[:][papers.Title.str.len() > 10]
papers = papers.sort(['Id'])

####################################################################################
# mark duplicate papers
####################################################################################
paper_alias = papers.groupby('Title').groups

papers['PaperAliasId'] = -1
papers['PaperAliasSize'] = -1
for title in paper_alias.keys():
    alias_ix = paper_alias[title]
    papers['PaperAliasId'][alias_ix] = [papers.Id[alias_ix[0]]] * len(alias_ix)
    papers['PaperAliasSize'][alias_ix] = [len(alias_ix)] * len(alias_ix)

papers = papers[:][papers.PaperAliasSize > 1]

####################################################################################
# join datasets and calculate groups
####################################################################################
author_groups = pd.merge(author_papers, papers, left_on='PaperId', right_on='Id')
author_groups = author_groups.drop(['Id', 'PaperAliasSize', 'Title'], axis=1)

author_groups = pd.merge(author_groups, authors, left_on='AuthorId', right_on='Id')
author_groups = author_groups.drop(['Id', 'Affiliation'], axis=1)
author_groups = author_groups.sort(['PaperAliasId', 'PaperId', 'AuthorId'])

author_groups_grouped = author_groups.groupby('PaperAliasId').groups
author_groups['KeepRecord'] = False
for alias_id in author_groups_grouped.keys():
    alias_ix = author_groups_grouped[alias_id]
    author_unique = np.invert(author_groups.ix[alias_ix].duplicated('AuthorId').values)
    paper_set = set()
    for ix in xrange(len(alias_ix)):
        cur_paper = author_groups.PaperId[alias_ix[ix]]
        if author_unique[ix] and not cur_paper in paper_set:
            paper_set.add(cur_paper)
            if len(paper_set) > 1:
                break
    if len(paper_set) > 1:
        for ix in xrange(len(alias_ix)):
            if author_unique[ix]:
                author_groups.KeepRecord[alias_ix[ix]] = True

author_groups = author_groups[:][author_groups.KeepRecord]
author_groups = author_groups.drop(['KeepRecord'], axis=1)

author_groups_csv = author_groups[['PaperAliasId', 'AuthorId', 'PaperId', 'Name']]
author_groups_csv.columns = ["authorgroup", "authorid", "subgroupid", "a_name"]
author_groups_csv.to_csv("author_groups.csv", header=["authorgroup", "authorid", "subgroupid", "a_name"],
                         index=False)

print "Total time ", time.time() - start_time, "seconds"

