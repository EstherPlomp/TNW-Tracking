import json
import requests
import yaml
import warnings
import os
import pandas as pd
import numpy as np
import concurrent.futures


# convert the list of DOI into a formatted JSON in the same format that
# https://github.com/meronvermaas/PURE_fulltext_analysis/tree/main/pure_harvester would do
# We can then run the pure_scraper approach as normal


def get_pure_metadata(doi, base_url, api_key):
    '''Get the metadata associated with a given DOI as returned by PURE API'''

    # Set up authentication
    headers = {
        'Accept': 'application/json',
        'api-key': api_key
    }

    # Step 1: Search for the publication using DOI
    search_url = f"https://{base_url}research-outputs"
    params = {
        'q': f'doi:("{doi}")',
    }


    print(f'\n::: Requesting API information for DOI: {doi}')
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()

    metadata = response.json()
    #print(metadata)
    if metadata['count'] == 0:
        warnings.warn(f"No publication found with DOI: {doi}")

    
    return metadata

def process_doi(doi, base_url, api_key, metadata):
    result = get_pure_metadata(doi, base_url, api_key)
    print(f'doing doi: {doi}')

    headers = {
        'Accept': 'application/json',
        'api-key': api_key
    }
    
    for count, item in enumerate(result['items']):
        if 'electronicVersions' in item:
            for eversion in item['electronicVersions']:
                if 'file' in eversion:                        
                    req_url = requests.get(eversion['file']['url'], headers=headers)
                    pub_path = os.path.join("pure_text_analysis/output", item['uuid'])
                    os.makedirs(pub_path, exist_ok=True)
                    # check length path + filename, should not exceed 255 characters
                    path_length = len(f'{os.getcwd()}/{pub_path}/{eversion["file"]["fileName"]}')
                    if path_length > 255:
                        eversion["file"]["fileName"] = eversion["file"]["fileName"][path_length-255:]
                    # download file
                    print(pub_path, eversion["file"]["fileName"], f'{pub_path}/{eversion["file"]["fileName"]}')
                    with open(f'{pub_path}/{eversion["file"]["fileName"].rsplit("/", 1)[-1]}', 'wb') as f:
                        f.write(req_url.content)
        #metadata: organisations, year, uuids (datasets)
        # organisations
        organisations_str = None
        organisations_names_str = None
        if 'organisationalUnits' in item:
            organisations = []
            organisations_names = []
            for organisation in item['organisationalUnits']:
                # contains external organisations as well
                organisations.append(organisation['uuid'])
                organisations_names.append(organisation['name']['text'][0]['value'])
            organisations_str = '|'.join(organisations)
            organisations_names_str = '|'.join(organisations_names)
                    # year
        pub_year = ''
        epub_year = ''
        for pubstatus in item['publicationStatuses']:
            pubstatus_text = pubstatus['publicationStatus']['term']['en_GB']
            # TODO figure out why this is breaking; did the API format change?
            # for text in pubstatus['publicationStatus']['term']['text']:
            #     if text['locale'] == 'en_GB':
            #         pubstatus_text = text['value']
            if pubstatus_text == 'E-pub ahead of print':
                epub_year = pubstatus['publicationDate']['year']
            elif pubstatus_text == 'Published':
                pub_year = pubstatus['publicationDate']['year']
                print(pub_year)
        # datasets
        datasets_str = None
        if 'relatedDataSets' in item:
            datasets = []
            for dataset in item['relatedDataSets']:
                datasets.append(dataset['uuid'])
            datasets_str = '|'.join(datasets)
        
        metadata.append({'uuid': item['uuid'],
                'pub_year': pub_year,
                'epub_year': epub_year,
                'organisations': organisations_str,
                'organisations_names': organisations_names_str,
                'datasets': datasets_str,
                'doi':doi})


def get_article_metadata(dois, base_url, api_key):
    '''Fetch the metdata information associated with a list of DOIs as returned by the PURE API and format
    it for downstream analysis.
    
    Code is almost verbatim copy of the get_outputs of https://github.com/meronvermaas/PURE_fulltext_analysis/blob/main/pure_harvester/outputs_api.py'''

    metadata = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for doi in dois:
            executor.submit(process_doi, doi, base_url, api_key, metadata)
             
    executor.shutdown(wait=True, cancel_futures=False)  # wait for workers to finish
    return metadata


if __name__ == '__main__':        

    # open the file containing PURE API base URL and API token
    with open('../pure-credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
        url = credentials["baseurl"][0]
        key = credentials["apikey"][0]

    # open the list of DOIs
    with open('../dois.yaml', 'r') as file:
        dois = yaml.safe_load(file)["dois"]

    # query the API and save formatted output to JSON
    metadata = get_article_metadata(dois, url, key)
    with open('pure_text_analysis/output/metadata.json', 'w') as f:
            f.write(json.dumps(metadata))

    # and as a dataframe CSV
    df = pd.DataFrame(metadata)
    df.drop_duplicates(subset="uuid")  # safety check
    #df["data_doi"] = np.nan  # TODO: bit of a dirty fix to try to prevent issues later
    df.to_csv(f'pure_text_analysis/output/merge.csv', index=False)

    # AFter tjos we can run `python -m pure_scraper``