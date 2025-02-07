Working on the output file several things were noticed: 

* Nemo:  The UUIDs seem to be not-unique: multiple UUIDS in the list of articles. 
  * Esther: For example: 17a3c19a-0084-42ff-bb06-7f3d780f6c45. This one has multiple DOIs associated with it and these multiple DOIs are all supposed to have GitLab links which they don't have (exactly the same links)

*  Esther: DOI's are also returning in multiple rows, for example 10.1038/s41534-022-00631-2 is listed 7 times 
*  Esther: False positives for a lot of the words - Gitea was found 5 times, of which only 2 times the word was in the article. Same for gitlab - loads of false positives 
*  Esther: For the 10.1038/s41534-022-00631-2 Gitlab was found to be positive while the word wasn't in the article, whereas 4TU.ResearchData is a False, which is mentioned in the data availability statement

From the hour that I spend on looking at the data it almost feels like I'm checking it manually without any prefiltered input, because of all the false hits and the missed keywords that are in the publication. 
