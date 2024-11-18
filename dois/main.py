import threading

import requests
import concurrent.futures
import csv


# from unidecode import unidecode


# get CrossRef API info
def get_crossref_info(doi):
	url = f"https://api.crossref.org/works/{doi}"
	try:
		response = requests.get(url, timeout=30)
	except:
		print('timeout or error getting Crossref info for:', url)
		return None

	if response.status_code == 200:
		data = response.json()
		return data['message']
	else:
		return None


# Crossref data extraction
# currently unused
def extract_info_from_crossref(data):
	if data:
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
	else:
		print("No data found for the provided DOI.")
		return None


def extract_authors(data):
	result = set()
	authors = data.get('author')
	for author in authors:
		result.add(author['family'])
	return result


def extract_reference_dois(data):
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
	dois_joined = ','.join(dois)
	url = f"https://doi.org/doiRA/{dois_joined}"
	try:
		response = requests.get(url, timeout=30)
	except:
		print('timeout or error getting DOI RA info for:', url)
		return dict()

	result = dict()
	data = response.json()
	for entry in data:
		result[entry.get('DOI')] = entry.get('RA')
	return result


def get_datacite_metadata(doi):
	url = f"https://api.datacite.org/dois/{doi}"
	try:
		response = requests.get(url, timeout=30)
	except:
		print('timeout or error getting metadata for:', url)
		return None

	if response.status_code == 200:
		data = response.json()
		return data.get('data').get('attributes')
	else:
		return None


# currently unused
def print_datacite_data(data):
	print('type: ', data.get('types').get('resourceType'))
	print('general type: ', data.get('types').get('resourceTypeGeneral'))
	print('Creators: ', data.get('creators'))


def extract_authors_from_datacite(data):
	creators = data.get('creators')
	result = []
	for creator in creators:
		result.append(creator.get("familyName"))
	return result


# Main script to get information from CrossRef and ORCID
# doi = "10.1016/j.dib.2024.110329"
# doi = "10.21468/SciPostPhys.16.5.135"


def get_matching_objects(doi):
	# Get CrossRef info
	crossref_data = get_crossref_info(doi)
	if crossref_data is None:
		return []
	# print('Crossref data: ', crossref_data)
	# print('Extracted authors: ', extract_authors(crossref_data))
	paper_authors = extract_authors(crossref_data)
	# print('paper authors:', paper_authors)
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


def get_and_save_output(doi, output, file, lock):
	print('Trying doi', doi)
	result = get_matching_objects(doi)
	output[doi] = result
	if len(result) > 0:
		print('matches found')
		lock.acquire()
		file.write(doi + ' : ' + ', '.join(result) + '\n')
		lock.release()
	else:
		print('no matches found')


all_dois = []
### EDIT THIS LINE BEFORE RUNNING TO ADAPT THE INPUT FILE ###
with open('./20241016-TNW_Articles_2020-2023_DOI-GH.csv') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for line in csv_reader:
		all_dois.append(line['DOI'])

output = dict()
### EDIT THIS LINE BEFORE RUNNING TO ADAPT THE OUTPUT FILE ###
matches_output_file = open('./20241016-TNW_Articles_2020-2023_DOI-GH-result-matches.txt', 'w', buffering=1)
lock = threading.Lock()
# 5 is the max, because Crossref only allows max 5 parallel connections
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
	for doi in all_dois:
		executor.submit(get_and_save_output, doi, output, matches_output_file, lock)

executor.shutdown(wait=True, cancel_futures=False)
matches_output_file.close()

print('Full report:')
print(output)

print('Report with matches only, line by line:')
for doi, matches in output.items():
	if len(matches) > 0:
		print(doi, ':', matches)
