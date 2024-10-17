# Finding related datasets by article text content

Since not everyone cites their own data or code in their references, it is also worthwhile to search for references to these in the text content of the pdf. This is, of course, a significantly more challenging task as natural language is trickier to parse. Luckily for us, Meron Vermaas has already made a good starting framework for us to use. It is [available on GitHub](https://github.com/meronvermaas/PURE_fulltext_analysis.git) and included as a submodule for this repository.

Since we are starting from a list of DOIs, we cannot use the `pure_harvester` that is part of Meron's code. Instead we roll a very fragile script that takes our list of DOIs  and harvests the metadata from PURE in much the same way and formats it as the [pure harvester](pure_text_analysis/pure_harvester) would.



## TODO

Did the API change in the time since Meron's code, or am I querying a different version somehow? Some fields have different names now. Don't know how to specify API version for PURE.

There are still some issues with the `data_doi` bits. You can comment the sections in the submodule, but a more proper fix is required