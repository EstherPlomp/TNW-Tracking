import yaml
import pandas as pd
import numpy as np

# Script that combines the data from both data exploration paths
# And produces some output files that can then be useful for further downstream analysis. 

### open the citation-based data

with open('find_by_citation/output/full_results.yml', 'r') as file:
    data_citation = yaml.safe_load(file)
   
### open the pdf-content based data

data_pdf = pd.read_csv('find_by_pdf_content/output/keywords_in_text.csv')

# filter the dataframe a bit
data = data_pdf.replace(False, np.nan).replace('[]', pd.NA)

# first we need to manually add the DOI into the dataset, as https://github.com/meronvermaas/PURE_fulltext_analysis
# does not include that in their output, but we do keep it in our get_article_metadata.py output

doi_data = pd.read_csv('find_by_pdf_content/pure_text_analysis/output/merge.csv')
doi_data.drop_duplicates(subset="uuid")  # safety check
data['doi'] = pd.NA
for index, row in data.iterrows():
    match = doi_data.loc[doi_data["uuid"] == row['uuid']]
    doi = match["doi"].values[0]
    data.at[index, 'doi'] = doi

print(data)

### Combine data into single dataframe
# now we can integrate our data_citation values into the main dataframe

data['cited_data'] = pd.NA
for index, row in data.iterrows():
    if row['doi'] in data_citation:  # doi matches
        # check if we actually found any dataset for this article
        if len(data_citation[row['doi']]) > 0:
            data.at[index, 'cited_data'] = ','.join(data_citation[row['doi']])

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
    if ((not pd.isna(row['github_url'])) or (not pd.isna(row['gitlab_url']))):
        articles[row['doi']].append({'git repositories':[]})
        repos = articles[row['doi']][-1]['git repositories']

        if not pd.isna(row['github_url']): 
            urls = format_string_list(row['github_url'])
            for url in urls:
                repos.append(url)
        if not pd.isna(row['gitlab_url']):
            urls = format_string_list(row['gitlab_url'])
            for url in urls:
                repos.append(url)

def process_keywords(df, data, excluded_cols):
    keywords = list(row.dropna().index)
    keywords = [kw for kw in keywords if kw not in excluded_cols]
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
    excluded_cols = ['uuid','doi','github_url', 'gitlab_url', 'pub_year', 'epub_year']
    process_keywords(articles, data, excluded_cols)


with open('output/combined_data.yml', 'w') as outfile:
    yaml.dump(articles, outfile, default_flow_style=False)
    