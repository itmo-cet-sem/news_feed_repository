# Our Personal News Feed

A web-based news feed to pick up news from a variety of sources and sort them according to the content.

## Structure

The project comprises the following components:
  * A web scrapper.
  * Javascript code running in a nodeJS server.
  * An HTML/CSS template with support for several screen sizes, i.e. with small screens support. This is loaded by the javascript code.
  * Code to analyze the content of each document collected, and:
    1. Learn using as reference the classification used by a single news-source, and store the patterns.
    2. Classify each content according to the learnt reference.
  
## General behavior

- The content refreshes every 12 hours.
- The news served by each request get sorted randomly.
- The bandwidth usage in the server is kept at minimum by loading the images of the news directly from the source.


### Additional notes
* The HTML template uses a bunch of code borrowed from all over the internet, in most cases adapted for the current need, all the respective disclaimers and licencing notes supplied remain in their places in the source files.
