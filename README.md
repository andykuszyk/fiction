# [akuszyk.com](https://akuszyk.com)
This repository holds the static files and site generator for my fiction site, [akuszyk.com](https://akuszyk.com).

It consists primarily of:
* `index.html` - the static landing page for the site;
* `generate-site.py` - the site generator for turning HTML book files (generated from LaTeX and `pandoc`) into formatted pages, with comments, tracking, etc.

## Usage
The `make` targets beginning with `generate-` should be used to generate the sites in sub-directories.

## Development
`make watch` can be used to run the site locally on port 80.
