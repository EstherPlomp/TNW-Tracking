import requests
import concurrent.futures
import yaml

# from unidecode import unidecode


def get_crossref_info(doi):
    """Fetches information about a DOI from the CrossRef API.

    Args:
        doi (str): The DOI to query.

    Returns:
        dict | None: A dictionary containing the retrieved information
                      or None if the request failed.
    """
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['message']
    else:
        return None


def extract_info_from_crossref(data):
    """Extracts information from a CrossRef API response.

    Args:
        data (dict): The response data from the CrossRef API.

    Returns:
        dict | None: A dictionary containing extracted information
                      or None if no data was found.
    """
    if not data:
        print("No data found for the provided DOI.")
        return None

    title = data.get('title', [''])[0]
    authors = data.get('author', [])
    author_names = [f"{author['given']} {author['family']}" for author in authors]
    publisher = data.get('publisher', '')
    publication_date = data.get('published-print', {}).get('date-parts', [['']])[0]

    print("Title:", title)
    print("Authors:", ", ".join(author_names))
    print("Publisher:", publisher)
    print("Publication Date:", "-".join(map(str, publication_date)))
    return authors


def extract_authors(data):
    """Extracts a set of author names from a CrossRef response.

    Args:
        data (dict): The response data from the CrossRef API.

    Returns:
        set(str): A set containing author family names.
    """
    result = set()
    authors = data.get('author')
    for author in authors:
        result.add(author['family'])
    return result


def extract_reference_dois(data):
    """Extracts DOIs from the references section of a CrossRef response.

    Args:
        data (dict): The response data from the CrossRef API.

    Returns:
        list(str): A list of extracted DOI strings.
    """
    print("References: ", data.get('reference'))
    references = data.get('reference')
    if references is None:
        return []

    result = []
    for reference in references:
        doi = reference.get('DOI')
        if doi is None:
            continue
        result.append(doi)

    return result


def extract_doi_registration_agency(dois):
    """Fetches registration agency information for a list of DOIs.

    Args:
        dois (list(str)): A list of DOI strings.

    Returns:
        dict(str, str): A dictionary mapping DOIs to their registration agencies.
    """
    dois_joined = ','.join(dois)
    url = f"https://doi.org/doiRA/{dois_joined}"
    response = requests.get(url)

    result = dict()
    data = response.json()
    for entry in data:
        result[entry.get('DOI')] = entry.get('RA')
    return result


def get_datacite_metadata(doi):
    """Fetches metadata about a DOI from the DataCite API.

    Args:
        doi (str): The DOI to query.

    Returns:
        dict | None: A dictionary containing the retrieved metadata
                      or None if the request failed.
    """
    url = f"https://api.datacite.org/dois//{doi}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['data'].get('attributes')
    else:
        return None


def print_datacite_data(data):
    """Prints specific fields from Datacite data.

    Args:
        data (dict): A dictionary containing Datacite data.
    """
    print('type: ', data.get('types').get('resourceType'))
    print('general type: ', data.get('types').get('resourceTypeGeneral'))
    print('Creators: ', data.get('creators'))


def extract_authors_from_datacite(data):
    """Extracts authors' family names from Datacite data.

    Args:
        data (dict): A dictionary containing Datacite data.

    Returns:
        list: A list of authors' family names.
    """
    creators = data.get('creators')
    result = []
    for creator in creators:
        result.append(creator.get("familyName"))
    return result


# Main script to get information from CrossRef and ORCID
# doi = "10.1016/j.dib.2024.110329"
# doi = "10.21468/SciPostPhys.16.5.135"


def get_matching_objects(doi):
	"""Retrieves matching objects based on author information and DOI.

    Args:
        doi (str): The DOI of the target paper.

    Returns:
        list: A list of matching DOIs.
    """
	# Get CrossRef info
	crossref_data = get_crossref_info(doi)
	print('Crossref data: ', crossref_data)
	print('Extracted authors: ', extract_authors(crossref_data))
	paper_authors = extract_authors(crossref_data)
	print('paper authors:', paper_authors)
	reference_dois = extract_reference_dois(crossref_data)
	doi_to_ra = extract_doi_registration_agency(reference_dois)
	matching_dois = []
	for reference_doi, registration_agency in doi_to_ra.items():
		if (registration_agency == 'Crossref'):
			print('Crossref found for DOI', reference_doi)
		elif (registration_agency == 'DataCite'):
			print('DataCite found for DOI', reference_doi)
			raw_datacite_data = get_datacite_metadata(reference_doi)
			reference_authors = extract_authors_from_datacite(raw_datacite_data)
			print('reference authors:', reference_authors)
			any_match = False
			for reference_author in reference_authors:
				if reference_author in paper_authors:
					any_match = True
					print('Matching author found:', reference_author)
			if any_match:
				matching_dois.append(reference_doi)
		else:
			print('For DOI we found:', registration_agency)
	return matching_dois


def get_and_save_output(doi, output):
	print('Trying doi', doi)
	result = get_matching_objects(doi)
	output[doi] = result
      
	  
## Main Matter

with open('../dois.yaml', 'r') as file:
    all_dois = yaml.safe_load(file)["dois"]
    
print(len(all_dois))

output = dict()
# 5 is the max, because Crossref only allows max 5 parallel connections
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
	for doi in all_dois:
		executor.submit(get_and_save_output, doi, output)

executor.shutdown(wait=True, cancel_futures=False)
print('Full report:')
print(output)

with open('output/full_results.yml', 'w') as outfile:
    yaml.dump(output, outfile, default_flow_style=False)

# collect only those entries that have a matching dataset (and hence a non-empty value for the dict val)
matches = {k: v for k, v in output.items() if v}

print('Report with matches only, line by line:')
print(matches)

with open('output/matches_results.yml', 'w') as outfile:
    yaml.dump(matches, outfile, default_flow_style=False)
            


