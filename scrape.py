import os

from requests import get
from bs4 import BeautifulSoup
import csv

def scrape_content():
  url = "https://en.wikipedia.org/wiki/List_of_fabrics"

  # Get list of links to scrape
  response = get(url)
  page_content = BeautifulSoup(response.text, 'html.parser')

  fabrics_content = page_content.find('div', class_ = 'mw-parser-output')
  all_links = fabrics_content.find_all('a')

  with open('fabrics.csv', 'w') as data_file:
    for link in all_links:
      try:
        if link['href'][0:6] == '/wiki/':
          fabric_name = link['title']

          # Ignore first link to generic textile
          if fabric_name in ['Textile', 'Fibre']:
            continue

          fabric_link = "https://en.wikipedia.org/" + link['href']
          dedicated_fabric_content  = BeautifulSoup(get(fabric_link).text, 'html.parser')
          fabric_description = dedicated_fabric_content.find('div', class_ = "mw-parser-output").find('p').get_text()

          data_file_writer = csv.writer(data_file)
          data_file_writer.writerow([fabric_name, fabric_description, fabric_link])

      except KeyError:
        # It comes to the last fabric anyway
        break

  return True

print(scrape_content())
