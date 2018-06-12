import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Union

import arxiv
import Levenshtein
from tqdm import tqdm

from conf2arxiv.postprocessing import stringify_authors


class ArXivPaper:

    def __init__(self, title: str, authors: List[str], uri: str):
        self.title = title
        self.authors = authors
        self.uri = uri


def parse_api_result(api_result: Dict[str, Any]) -> ArXivPaper:
    title = api_result['title']
    authors = api_result.get('authors', [])
    uri = [link['href'] for link in api_result['links']
           if link['type'] == 'text/html']
    return ArXivPaper(title, authors, uri[0])


def search_arxiv(title: str, authors: List[str]=[]) -> Union[None, ArXivPaper]:

    DIST_TITLE_ALLOWABLE = 5
    DIST_AUTHORS_ALLOWABLE = 15
    REPL_PATTERN = r'''[,.?'"()-]+'''

    title_for_query = re.sub(REPL_PATTERN, ' ', title).strip().lower()

    api_results = arxiv.query('all:{}'.format(title_for_query), max_results=5)
    arxiv_papers = [parse_api_result(a) for a in api_results]

    for arxiv_paper in arxiv_papers:

        dist_title = \
            Levenshtein.distance(arxiv_paper.title.strip().lower(),
                                 title.strip().lower())
        dist_authors = \
            Levenshtein.distance(' '.join(sorted(arxiv_paper.authors)),
                                 ' '.join(sorted(authors))) \
            if len(authors) == 0 \
            else 0

        if dist_title < DIST_TITLE_ALLOWABLE and dist_authors < DIST_AUTHORS_ALLOWABLE:
            return arxiv_paper

    return


def main() -> None:
    parser = argparse.ArgumentParser(prog='conf2arxiv')
    parser.add_argument('conference', type=str, choices=['acl2018'])
    args = parser.parse_args()

    with Path(args.json_path).open(mode='r') as f:
        entries = json.load(f)

    results = []
    for entry in tqdm(entries):
        title = entry['title']
        authors = entry.get('authors', [])
        arxiv_paper = search_arxiv(title, authors)
        if arxiv_paper is not None:
            results.append((title, authors, arxiv_paper))

    dest = Path(args.csv_dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open(mode='w') as f:
        HEADER = ['title in the list',
                  'authors in the list',
                  'title found',
                  'authors found',
                  'uri']
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(HEADER)
        for (title, authors, arxiv_paper) in results:
            writer.writerow([title,
                             stringify_authors(authors),
                             arxiv_paper.title,
                             stringify_authors(authors),
                             arxiv_paper.uri])


if __name__ == '__main__':
    main()
