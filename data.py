import requests
from bs4 import BeautifulSoup

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

def get_official_languages(state):
    url = f"https://en.wikipedia.org/wiki/{state}"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
    else:
        return "Failed to get data from url"

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find_all("table")[1]
    rows = table.find_all('tr')
    for row in rows:
        print(row.prettify())
        header = row.find("th", "infobox-label")
        if header and header.get_text() in "Official language":
            print("FOUND OFFICIAL LANGUAGE")
            print(row.find("td", "infobox-data"))
            break
    return None
