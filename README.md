# TNW-Tracking
Tracking Research Objects at the Faculty of Applied Sciences, TU Delft

Evaluation of researcher performance is currently a contested subject within academia. Although many researchers contribute to their field of expertise in a multitude of manners, the most stringent criteria of success is the number of research articles published. Subverting the current “publish or perish” culture requires a novel approach to the evaluation of research objects (such as software, data and methods) other than research articles. However, there is currently no standardised way to track such research objects. This project aims to identify and quantify the role of research objects, in particular research software, within the Faculty of Applied Sciences at TU Delft and evaluate how these are being shared within the research community. By monitoring open research objects such as software, the project aims to stimulate an open research culture and incentivise scientists to adhere to Open Science practices and the FAIR principles.


## Proposal
[eScience Center Fellowship Programme 2024: Application Form Esther Plomp](https://doi.org/10.5281/zenodo.10939832)

## Approach ⚙

The approach used to try to get an idea of how 'well' the faculty is doing is given below. One would manually request a list of DOIs of articles published by the department.

Note that the pdf text content search uses [existing work by Meron Vermaas](https://github.com/meronvermaas/PURE_fulltext_analysis/tree/main)

```mermaid
graph TD;
    DOIs-->dd[Search Citations];
    crossref-->de[Find Dataset References]
    datacite-->de[Find Dataset References]
    dd[Search Citations]-->de[Find Dataset References]
    DOIs-->df[Download PDF];
    PURE-->df[Download PDF];
    df[Download PDF]-->dg[Search for keywords]
    dg[Search for keywords]-->dh[Guage Open Sciene Progress];
    de[Find Dataset References]-->dh[Guage Open Sciene Progress];  
```

## Setup 📦

**Python**

All the code is run by a Python frontend. Code is tested on Python `3.10.15`

I suggest you create a new virtual environment and then install the required packages and dependencies into it using:

```shell
python setup.py
```

**PURE information**

You will also need to specify the pure server URL and provide an authentication token. These are entered in [pure-credentials.yaml](pure-credentials.yaml)

**DOIs**

Finally, you have to provide a list of DOIs that the scripts will use as input. These are to be entered into [dois.yaml](dois.yaml)

## Running 🚀

To run the analysis on your list of DOIs, you can simply call the following in the root directory:

```shell
python main.py
```

> [!IMPORTANT]  
> The code is very much not optimised, and it may take quite a while to run, depending on how many DOIs you want evaluated. On a fast laptop it takes around 10 minutes for 80 DOIs.

# Prior Art ⬇


## Relevant keywords for TNW

Keywords: GitHub, Lab, bitbucket, subversion, gitea, gogs
data” “code” “method” “data repository”, “available”, “DOI”, as well as data repositories regularly used by researchers of the faculty (4TU.ResearchData - 4TU ResearchData, Zenodo, ENA, EVA, SRA, UniProtKB, IDR, EMPIAR). 

## Relevant repositories/platforms
- GitHub
- GitLab
- 4TU.ResearchData - via DataCite: https://api.datacite.org/dois?provider-id=HNYE / https://support.datacite.org/reference/get_dois

## Relevant Projects and Resources

- [Charité Metrics Dashboard](https://quest-dashboard.charite.de/) (using [ODDPub](https://github.com/quest-bih/oddpub)) 
  - ODDPub allows to obtain estimates of the prevalence of Open Data in the biomedical literature on a larger scale and independent of data availability statements. The ODDPub algorithm is freely available as R package on GitHub (https://doi.org/10.5281/zenodo.4071699, RRID:SCR_018385). https://github.com/quest-bih/oddpub/tree/v6
- [French Open Science monitor](https://frenchopensciencemonitor.esr.gouv.fr/) (using [GROBID](https://github.com/kermitt2/grobid) and [softcite](https://github.com/softcite/software-mentions)). See [Bassinet et al. 2023](https://hal.science/hal-04121339v3).
  - Softcite dataset [Howison et al. 2023](https://zenodo.org/doi/10.5281/zenodo.7995564), [Du et al. 2021](https://doi.org/10.1002/asi.24454) - and Softcite software mention recognizer [Lopez et al. 2021](https://doi.org/10.1145/3459637.3481936)
  - Note on softcite: only coverage/accuracy in Life Sciences and Economics, and to implement larger scale you'll need your own server
  - [University of Lorraine adaption](https://gitlab.com/Cthulhus_Queen/barometre_scienceouverte_universitedelorraine) (see [website](https://scienceouverte.univ-lorraine.fr/en/bibliometrics/lorraine-open-science-barometer/))

- [Culina et al. 2020](https://doi.org/10.1371/journal.pbio.3000763)
- [Riedel et al. 2020](https://doi.org/10.5334/dsj-2020-042)
- [Serghiou et al. 2021](https://doi.org/10.1371/journal.pbio.3001107)
- [Du et al. 2022](http://dx.doi.org/10.7717/peerj-cs.1022)
- [DataStet](https://github.com/kermitt2/datastet)
- [Open Science Monitoring Initiative](https://open-science-monitoring.org/)
- SoMeSci dataset [Schindler et al. 2021](https://doi.org/10.1145/3459637.3482017)
- [Maitner et al. 2024](https://doi.org/10.1002/ece3.70030) 
    -   We find that code is rarely published (only 6% of papers), with little improvement over time. 
    - agent-based models found that 81% did not provide code (Barton et al., 2022)
    - Open access information was provided by the rscopus R package (Muschelli, 2019).
    - All R scripts underlying these analyses are available at: https://github.com/bmaitner/R_citations and via Zenodo ([Maitner & Lei, 2024](https://zenodo.org/doi/10.5281/zenodo.8201250))
    - Overall, R code was only available for 55 of the 1001 papers examined (5.5%; Figure 1). When shared, code was most often in the Supplemental Information (40%), followed by Github (22%), Figshare (11%), or other repositories (37%).
      The majority of code (67%) did not include a license. Where a license was included, it was nearly always permissive or copyleft (e.g., CC0, CC-BY, GPL, and MIT).

- "In this analysis, we leverage two text and data mining tools, Publink and xDD, to identify data citations that may not be present in structural metadata records. Publink is a Python
package that allows users to find relationships between publications and data (Wieferich et al. 2020). In cases where references are not included in the publication’s DOI structural metadata,
Publink can be used to see if researchers are referencing their data by searching for mentions of data DOIs in the full text of publications included in the eXtract Dark Data (xDD) digital library.
xDD, formerly known as GeoDeepDive, is a cyberinfrastructure that compiles data on published literature and provides users with the ability to perform full text searches of published literature
using the xDD API (Peters et al. 2021a)." - [Donovan and Langseth 2024](https://doi.org/10.5334/dsj-2024-024)
    - Wieferich, D, Serna, B, Langseth, M, et al. 2020 Publink. U.S. Geological Survey Software Release. DOI: https://doi.org/10.5066/P92MX1NF (Azin/Joshua worked on some of these scripts)

### Relevant publications
- [Katz and Chue Hong 2024](http://dx.doi.org/10.7717/peerj-cs.1951) - future recommendations for better software citations

### Project Meron Vermaas, eScience Fellow 2023-2024
https://github.com/meronvermaas/PURE_fulltext_analysis
- Van de repositories de collaborators extracten en dan keywords zoeken voor mensen die bij faculteit werken. 
- Output.api.py – metadata
- API key voor pure nodig – maar kan ook via OpenAIRE voor open access publicaties. 

### Code availability
- [vandewalle 2019](https://lirias.kuleuven.be/2815281?limo=0) - Code availability increased to 24% and increased citation for publications with code. Reanalysis of a previous study in 2012 found out that "Out of the 66 links to code found in 2012, only
47 were still valid (or easy to fix)."
- [Laurinavichyute et al. 2022 ](https://doi.org/10.1016/j.jml.2022.104332) - reproducibility rate ranged from 34% to 56%

### SWORDS

* [A curated list of awesome open source projects from Utrecht University](https://github.com/UtrechtUniversity/awesome-utrecht-university)
* [Template of the SWORDS code](https://github.com/UtrechtUniversity/SWORDS-UU)
* [TNW template set up based on SWORDS](https://github.com/EstherPlomp/SWORDS-TNW)

### Datasets TNW on 4TU.ResearchData
- https://research.tudelft.nl/en/organisations/applied-sciences/datasets/

### Sharing Data/Software in other resources

- [Colavizza et al. 2020](https://doi.org/10.1371/journal.pone.0230416). We defined a categorisation for Data Availability Statements (DAS) and trained a classifier to automatically categorise articles.
- [Colavizza et al. 2024](https://doi.org/10.48550/arXiv.2404.16171), Table 4

| Syntax      | % of publications |
| ----------- | ----------- |
| Publications     | 100%       |
| Sharing data (anywhere)   | 68%       |
| Sharing data (repository)   | 22%        |
| Sharing data (online)   | 28%        |
| Sharing code   | 12%       |
| Preprinted   | 20%       |

- [Briney 2024](https://doi.org/10.22002/d2h9g-5q152), For DOIs, regular expressions such as “10.1371” from “10.1371/journal.
- [Gabelica et al. 2022](https://doi.org/10.1016/j.jclinepi.2022.05.019) based on BioMedCentral data using [BMC scrapper](https://github.com/bojcicm/bmc-scrapper)
- https://github.com/caltechlibrary/pubarchiver/blob/main/scripts/upload-to-pmc
- research-software-directory.org (but only at [TU Delft level](https://research-software-directory.org/organisations/delft-university-of-technology))
  - RST: [GEMDAT](https://zenodo.org/doi/10.5281/zenodo.8401669) (Anastasiia K. Lavrinenko and Theodosios Famprikis)
  

## Other notes

- Publication corpus completeness
  - Access to full-texts often difficult
  - Limited coverage of documents without DOI
  - Current dataset & software extraction supports only English
  - Performance across domains
- Software is more than what is visible from publications: library/package dependencies

## TNW Software
- [DIPlib](https://diplib.org/contributors.html) ImPhys (Bernd Rieger, Ronald Ligteringen) (found via softcite dataset)
