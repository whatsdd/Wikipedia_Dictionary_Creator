import os
import re
import urllib.request
import time
from urllib.parse import urljoin

# Function to fetch Wikipedia language dumps with retry logic
def get_wikipedia_dumps(retries=3, delay=5):
    url = "https://dumps.wikimedia.org/other/static_html_dumps/current/"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                html = response.read().decode("utf-8")
            links = re.findall(r'href="(.*?)"', html)
            links = [link for link in links if link != "../"]
            return url, links
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print("Failed to retrieve Wikipedia dumps after multiple attempts.")
    return url, []

# Function to display available language options to the user
def display_language_options(links):
    if not links:
        print("No Wikipedia language dumps available.")
        return
    print("Available Wikipedia language dumps:")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")

# Function to download titles for the selected Wikipedia language
def download_titles(url, language, save_path, retries=3, delay=5):
    language_url = urljoin(url, f"{language}/html.lst")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(language_url, timeout=10) as response:
                content = response.read().decode("utf-8")
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Downloaded {language_url} to {save_path}")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print(f"Failed to fetch {language_url} after multiple attempts.")
    return False

# Function to clean extracted titles and generate a dictionary file
def clean_titles(file_path, output_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return
    
    cleaned_titles = set()
    ip_regex = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    split_chars = re.compile(r"[;,.!@#%&()]")  # Removed underscores, dashes, and parentheses
    
    for line in lines:
        clean = line.strip()
        clean = clean.split("/")[-1].split(".")[0]
        if "~" in clean:
            clean = clean.split("~")[-1]
        
        clean = clean.replace("_", "").replace("-", "")  # Removing underscores and dashes
        clean = clean.replace("(", "").replace(")", "")  # Removing parentheses
        
        if not ip_regex.match(clean):
            words = split_chars.split(clean)
            for word in words:
                cleaned_titles.add(word.strip())
    
    cleaned_titles = sorted(set(filter(None, cleaned_titles)))
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(cleaned_titles))
    
    print(f"Cleaned dictionary saved to {output_path}")

# Main function to manage user interaction and workflow
def main():
    working_dir = os.path.join(os.getenv("LOCALAPPDATA", "."), "wikipedia-dictionary-creator")
    os.makedirs(working_dir, exist_ok=True)
    
    url, links = get_wikipedia_dumps()
    if not links:
        return
    
    display_language_options(links)
    
    try:
        choice = int(input("Enter the number of the language to download: ")) - 1
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    if 0 <= choice < len(links):
        selected_language = links[choice].strip('/')
        lang_code = selected_language.upper()
        file_path = os.path.join(working_dir, f"{lang_code}-unfiltered.txt")
        dict_path = os.path.join(working_dir, f"{lang_code}-wordlist.txt")
        
        if not os.path.exists(file_path):
            if not download_titles(url, selected_language, file_path):
                return
        else:
            print(f"File {file_path} already exists. Reusing it.")
        
        clean_titles(file_path, dict_path)
        print("Process completed successfully.")
    else:
        print("Invalid selection.")

# Ensuring the script runs as a standalone program
if __name__ == "__main__":
    main()