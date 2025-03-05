# Wikipedia Wordlist Generator

A Python script to generate wordlists from Wikipedia static HTML dumps. This tool extracts article titles from Wikipedia dumps in various languages, cleans the text, and creates a dictionary file useful for penetration testing, password cracking, and linguistic analysis. Credits to ChrisAD for creating orginal PS version https://github.com/ChrisAD/wiki-dictionary-creator. 
## Features

- Fetches Wikipedia static HTML dumps automatically.
- Allows users to select a language from available Wikipedia dumps.
- Downloads and processes article titles into cleaned wordlists.
- Removes underscores, dashes, parentheses, and other unwanted characters.
- Splits concatenated words (e.g., `AbuSimbel,RamessesTemple,front,Egypt,Oct2004` → `AbuSimbel`, `RamessesTemple`, `front`, `Egypt`, `Oct2004`).
- Saves two output files:
  - `{LANGCODE}-unfiltered.txt`: The raw list of titles.
  - `{LANGCODE}-wordlist.txt`: The cleaned and formatted dictionary.

## Installation

This script requires no external dependencies beyond Python's standard library. Simply download and run python3 Wikipedia-Wordlist-Generator.py inside the directory or with full path.


### Clone the repository:

```sh
git clone https://github.com/yourusername/wikiwordlists.git
cd wikiwordlists

python3 Wikipedia-Wordlist-Generator.py
or 
python3 Wikipedia-Wordlist-Generator.py

