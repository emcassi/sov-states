import requests
from bs4 import BeautifulSoup
from models import Language, State
from db import db

def get_list_of_states():
    url = "https://en.wikipedia.org/wiki/List_of_sovereign_states"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
    else:
        return "Failed to get data from url"

    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all("table")[1].find('tbody')

    states = []

    for row in rows:
        data = row.find('td')
        if data and not isinstance(data, int):
            state = data.find('a').get_text()
            states.append(state)

    return states

def is_valid_language(language):
    cleaned = clean_language(language).lower()
    
    if "languages" in cleaned:
        return False
    if "others" in cleaned:
        return False
    if "federal level" in cleaned:
        return False
    if cleaned == "see full list": 
        return False
    return True

def check_row_for_languages(row):
    header = row.find("th")
    data = row.find("td")
    if header and header.get_text():
        if data and not isinstance(data, int):
            header_text = header.get_text().lower()
            if "languages" in header_text:
                list = data.find_all('a')
                languages = []
                for item in list:
                    if item.parent.name == 'i':
                        continue

                    if item.has_attr('title'):
                        cleaned = clean_language(item.get_text())
                        if is_valid_language(cleaned):
                            languages.append(cleaned)

                return languages
            elif "language" in header_text:
                cleaned = clean_language(data.get_text())
                if is_valid_language(cleaned):
                    return [cleaned]
                else:
                    return []
            
    return None


def clean_language(language):
    if '[' in language:
        language = language[:language.index('[')]
    if '(' in language:
        language = language[:language.index('(')]
    if '\n' in language:
        language = language[0:language.index('\n')] + language[language.index('\n') + 1:]
    return language.strip()

def get_languages(state):
    url = f"https://en.wikipedia.org/wiki/{state}"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
    else:
        return "Failed to get data from url"

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find_all('table', 'vcard')
    if not table:
        if state.endswith('country'):
            return None
        else:
            return get_languages(state + " (country)")
    table = table[0].find('tbody')
    rows = table.find_all('tr')
    languages = []
    for row in rows:
        new_languages = check_row_for_languages(row)
        if new_languages:
            languages.extend(new_languages)
        
    return languages

