
# SWORDS

The SWORDS workflow focuses on GitHub - which requires a lot of manual processing of the retreived information as people do not indicate information about which university they are from, let alone which faculty or which department. It may be worthwhile to test out the third SWORDS script to check how FAIR the repositories are, but also: https://github.com/fair-software/howfairis or https://github.com/fair-software/fairtally (which runs howfairis over a list of repositories)

# Exploring workflow Meron

Meron's workflow requires access to PURE API, which we did not manage to obtain. Additionally, the information received needs to be slightly updated - we are not necessairly looking at the amount of keywords in articles, but more towards percentages of data/code sharing for a particular list of articles. 

# Exploring 4TU.ResearchData

Uploads registered in 4TU.ResearchData are assigned at the institutional level, and does not have more granular level at the Faculty/Department level. Esther has set up an overview with the existing uploads for our faculty thanks to Jan, data curator at 4TU.ResearchData, who manually kept a list with more granular information. We are allowed to share this dataset publicly. 

# Exploring Zenodo

Similar issues as 4TU.ResearchData - metadata missing or not detailed enough. Esther is working on a manual overview. 

# 1 October eSciencecenter (Ewan/Nemo/Esther/Carlos

* Example paper which cites code repository in the references: https://scipost.org/10.21468/SciPostPhys.16.5.135 /  10.21468/SciPostPhys.16.5.135 + example 2: https://doi.org/10.1103/PhysRevB.99.075416

However: Not all researchers cite their data/code in the references - most will only mention a link or DOI to a dataset/repository. 

* Example paper which has a data availability statement: https://doi.org/10.1002/smtd.202300258

Journals such as Soft Matter and PHYSICAL REVIEW B do not have these standardised 'data availability statement' or they call it differently (data and material availability statement). 

Possibly both approaches combined would give the most information: checking the references (and checking the authors of the references in case the authors are citing someone elses data/code), and checking the text for data availability statements or keywords (zenodo, 4TU.ResearchData). 
