RottenTomatoesScraper
=====================

#RottenTomatoesScraper
##Objects for Mutliple Results (MovieSearchResult) and single movie pages (MoviePage) with Preview methods.

The initial search query is raw_input but could be changed to command-line argument. Function returns custom object MoviePage, which could be serialized to json.

Any string output is likely to need unicode parsing - MoviePage.cast for example.

The API from RottenTomatoes is a superior way of collecting the info, but requires a key.
