import threading

import requests
import concurrent.futures


# from unidecode import unidecode


# get CrossRef API info
def get_crossref_info(doi):
	url = f"https://api.crossref.org/works/{doi}"
	try:
		response = requests.get(url, timeout=10)
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
		response = requests.get(url, timeout=10)
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
		response = requests.get(url)
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


all_dois = [
	'10.1021/acssynbio.2c00668',
	'10.1038/s41580-023-00686-9',
	'10.1093/synbio/ysad006',
	'10.1038/s41598-023-43682-x',
	'10.1021/acs.nanolett.3c02630',
	'10.1039/d2sm01562e',
	'10.1038/s41467-023-37910-1',
	'10.1016/j.bpj.2023.02.018',
	'10.1038/s41598-023-35359-2',
	'10.1016/j.tim.2022.12.006',
	'10.1039/d2lc01060g',
	'10.1038/s41467-023-42100-0',
	'10.1038/s41564-023-01501-z',
	'10.1098/rstb.2022.0044',
	'10.1038/s41589-022-01225-x',
	'10.1038/s41586-023-05961-5',
	'10.1038/s41565-023-01510-3',
	'10.1016/j.bpj.2022.11.1824',
	'10.1016/j.bpj.2022.11.1828',
	'10.1126/science.adi8308',
	'10.1016/j.bpj.2022.11.1664',
	'10.1016/j.jtha.2023.06.011',
	'10.1038/s41598-023-27734-w',
	'10.1016/j.optcom.2023.129548',
	'10.1242/jcs.259639',
	'10.1002/adbi.202200172',
	'10.1021/acssynbio.3c00074',
	'10.1103/PhysRevX.13.021010',
	'10.3389/fbioe.2022.1110376',
	'10.1016/j.cell.2023.01.041',
	'10.1038/s41467-023-43440-7',
	'10.3389/fmicb.2023.1107093',
	'10.1016/j.bpj.2022.11.1716',
	'10.1146/annurev-biochem-032620-110506',
	'10.3389/fmicb.2023.1076570',
	'10.1016/j.bpj.2022.11.1071',
	'10.7554/eLife.87174.1',
	'10.1093/nar/gkad1055',
	'10.1371/journal.pone.0291625',
	'10.1039/d3py00075c',
	'10.1103/PhysRevB.108.L081401',
	'10.1021/acs.biomac.2c01405',
	'10.1016/j.tibtech.2022.08.008',
	'10.1099/mgen.0.000968',
	'10.1016/j.jtha.2023.10.025',
	'10.1016/j.optcom.2023.129474',
	'10.1038/s41467-023-35997-0',
	'10.1021/acs.chemmater.3c00502',
	'10.1122/8.0000559',
	'10.1103/PhysRevLett.131.124001',
	'10.1242/jcs.260154',
	'10.1093/bioadv/vbad017',
	'10.1038/s41587-023-01839-z',
	'10.1002/adma.202305505',
	'10.1088/2050-6120/acfb58',
	'10.15252/embj.2022112504',
	'10.1038/s41467-023-37093-9',
	'10.1016/j.bpj.2023.11.008',
	'10.20517/evcna.2023.26',
	'10.1016/j.isci.2023.108268',
	'10.1093/nar/gkad171',
	'10.1016/j.xplc.2023.100716',
	'10.1016/j.xcrp.2023.101552',
	'10.1002/adbi.202300105',
	'10.1038/s41565-023-01527-8',
	'10.1016/j.isci.2023.105958',
	'10.1002/smtd.202300258',
	'10.1038/s41467-023-42524-8',
	'10.1093/nar/gkad868',
	'10.1016/j.ohx.2023.e00428',
	'10.1364/OE.505958',
	'10.1038/s41598-023-39829-5',
	'10.1016/j.celrep.2023.113284',
	'10.1021/acs.jpcc.3c03815',
	'10.1021/acsnano.3c05959',
	'10.1126/sciadv.add6480',
	'10.1016/j.bpj.2022.11.1695',
	'10.1016/j.actbio.2022.12.009',
	'10.1038/s41598-023-49101-5',
	'10.1016/j.bioadv.2023.213289',
	'10.3389/fonc.2022.1101901',
	'10.1002/smtd.202300416',
	'10.1083/jcb.202208062',
	'10.7554/eLife.85183',
]


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


output = dict()
### EDIT THIS LINE BEFORE RUNNING ###
matches_output_file = open('./20241016-TNW_Articles_2020-2023_DOI-GH-result-matches.txt', 'a', buffering=1)
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
