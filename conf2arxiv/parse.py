from pathlib import Path
from typing import Any, Dict, List

from bs4 import BeautifulSoup


def parse_li(li: Any) -> Dict[str, str]:
    text_author = li.find('span', {'class': 'paper-authors'}).text
    authors = text_author.replace(' and ', ', ').split(', ')
    return {'title': li.find('span', {'class': 'paper-title'}).text,
            'authors': authors}


def parse_html(markup: Path) -> List[Dict[str, str]]:
    with markup.open(mode='r') as r:
        soup = BeautifulSoup(r, 'html5lib')
        ul = soup.find('ul', {'class': 'accepted-papers'})
        return [parse_li(li) for li in ul.find_all('li')]
