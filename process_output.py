import yaml
import pandas as pd
import numpy as np
import shutil
import warnings

# Script that combines the data from both data exploration paths
# And produces some output files that can then be useful for further downstream analysis. 

### open the citation-based data

with open('find_by_citation/output/matches_results.yml', 'r') as file:
    data_citation = yaml.safe_load(file)
   
### open the pdf-content based data

data_pdf = pd.read_csv('find_by_pdf_content/output/keywords_in_text.csv')

# filter the dataframe a bit
data_pdf = data_pdf.replace(False, np.nan).replace('[]', pd.NA)  # empty list -> NA
data_pdf = data_pdf.drop_duplicates(subset='doi', keep='first')  # remove duplicate DOI items (pick first one without deep motivation)

### Combine data into single dataframe

# now we can integrate our data_citation values into the main dataframe
data_pdf['cited_data'] = pd.NA
match_count = 0
for index, row in data_pdf.iterrows():
    if row['doi'] in data_citation:  # doi matches
        # check if we actually found any dataset for this article
        if len(data_citation[row['doi']]) > 0:
            data_pdf.at[index, 'cited_data'] = ','.join(data_citation[row['doi']])
            match_count += 1

# it is possible we did not find the matches found by citation method in our pdf scraping dataset
# because, for example, we were unable to download the pdf contents of an article. 
if match_count < len(data_citation):
    warnings.warn(f"{len(data_citation) - match_count} articles from the citation could not be found"
                   "in the pdf scraping collection. Something may have gone wrong in downloading their pdf contents.")

# now that data is combined, we rename the variable for legibility, and save it to storage
data = data_pdf
data.to_csv('output/combined_data.csv', index=False) 

### Reduce to yaml object and save

def format_string_list(raw_string):
    stringlist = raw_string.split(",")  # there can be multiple links
    urls = []

    for url_raw in stringlist:
        # clean up the string
        repo_url = url_raw.replace("[","").replace("]","").replace("'","").strip()
        urls.append(repo_url)

    # remove duplicates
    urls = list(set(urls))

    return urls

def process_git_repos(df, data):
    # check if we have at least one link to a git repository
    if ((not pd.isna(row['github_url'])) or (not pd.isna(row['bitbucket']))):
        articles[row['doi']].append({'git repositories':[]})
        repos = articles[row['doi']][-1]['git repositories']

        if not pd.isna(row['github_url']): 
            urls = format_string_list(row['github_url'])
            for url in urls:
                repos.append(url)
        if not pd.isna(row['bitbucket_url']):
            urls = format_string_list(row['bitbucket_url'])
            for url in urls:
                repos.append(url)

def process_keywords(df, data, excluded_cols, keywords_target):
    '''If keywords_target is an empty list, the keywords will not be filtered at all'''
    keywords = list(row.dropna().index)
    keywords = [kw for kw in keywords if kw not in excluded_cols]
    if len(keywords_target) > 0:
        keywords = [kw for kw in keywords if kw in keywords_target]
    if keywords:
        articles[row['doi']].append({'keywords': keywords})


articles = {}
cols = data.columns.to_numpy()  # for keywords later
for index, row in data.iterrows():
    articles[row['doi']] = []
    # check if we had any cited datasets/code
    if not pd.isna(row['cited_data']):
        articles[row['doi']].append({'cited':format_string_list(row['cited_data'])})

    # check if github or gitlab repositories are linked
    process_git_repos(articles, data)

    # collect the keywords, drpping some values 
    excluded_cols = ['uuid','doi','github_url', 'gitlab_url', 'pub_year', 'epub_year', 'data']
    keywords_target = []
    process_keywords(articles, data, excluded_cols, keywords_target)


# also copy the used keywords to the output folder for reference
shutil.copyfile("find_by_pdf_content/keywords.txt", "output/keywords_used.txt")

# save the final data to storage
with open('output/combined_data.yml', 'w') as outfile:
    yaml.dump(articles, outfile, default_flow_style=False)
    
# report to console
with open('dois.yaml', 'r') as file:
    dois = yaml.safe_load(file)

print(f"Completed processing, combined output for {len(articles)} dois from the original {len(dois['dois'])} input dois "
      f"({len(dois['dois'])-len(articles)} missing)")