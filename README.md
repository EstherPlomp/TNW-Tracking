# TNW-Tracking
Tracking Research Objects at the Faculty of Applied Sciences, TU Delft

Evaluation of researcher performance is currently a contested subject within academia. Although many researchers contribute to their field of expertise in a multitude of manners, the most stringent criteria of success is the number of research articles published. Subverting the current “publish or perish” culture requires a novel approach to the evaluation of research objects (such as software, data and methods) other than research articles. However, there is currently no standardised way to track such research objects. This project aims to identify and quantify the role of research objects, in particular research software, within the Faculty of Applied Sciences at TU Delft and evaluate how these are being shared within the research community. By monitoring open research objects such as software, the project aims to stimulate an open research culture and incentivise scientists to adhere to Open Science practices and the FAIR principles.


## Proposal
[eScience Center Fellowship Programme 2024: Application Form Esther Plomp](https://doi.org/10.5281/zenodo.10939832)


## Relevant keywords for TNW

Keywords: GitHub, Lab, bitbucket, subversion, gitea, gogs
data” “code” “method” “data repository”, “available”, “DOI”, as well as data repositories regularly used by researchers of the faculty (4TU.ResearchData, Zenodo, ENA, EVA, SRA, UniProtKB, IDR, EMPIAR). 

## Relevant repositories/platforms
- GitHub
- GitLab

## Relevant Projects and Resources

- [Charité Metrics Dashboard](https://quest-dashboard.charite.de/) (using [ODDPub](https://github.com/quest-bih/oddpub)) 
  - ODDPub allows to obtain estimates of the prevalence of Open Data in the biomedical literature on a larger scale and independent of data availability statements. The ODDPub algorithm is freely available as R package on GitHub (https://doi.org/10.5281/zenodo.4071699, RRID:SCR_018385). https://github.com/quest-bih/oddpub/tree/v6
- [French Open Science monitor](https://frenchopensciencemonitor.esr.gouv.fr/) (using [GROBID](https://github.com/kermitt2/grobid) and [softcite](https://github.com/softcite/software-mentions)).
  - Note on softcite: only coverage/accuracy in Life Sciences and Economics, and to implement larger scale you'll need your own server

- [Culina et al. 2020](https://doi.org/10.1371/journal.pbio.3000763)
- [Riedel et al. 2020](https://doi.org/10.5334/dsj-2020-042)
- [Serghiou et al. 2021](https://doi.org/10.1371/journal.pbio.3001107)

### Project Meron Vermaas, eScience Fellow 2023-2024
https://github.com/meronvermaas/PURE_fulltext_analysis
- Van de repositories de collaborators extracten en dan keywords zoeken voor mensen die bij faculteit werken. 
- Output.api.py – metadata
- API key voor pure nodig – maar kan ook via OpenAIRE voor open access publicaties. 

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

