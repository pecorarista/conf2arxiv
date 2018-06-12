import argparse
import csv
import json
from pathlib import Path

from tqdm import tqdm

from conf2arxiv.postprocessing import stringify_authors, same
from conf2arxiv.search import search_arxiv
from conf2arxiv.fetch import fetch_web_page
from conf2arxiv.parse import parse_html


def main() -> None:

    parser = argparse.ArgumentParser(prog='conf2arxiv')
    parser.add_argument('conference', type=str, choices=['acl2018'])
    args = parser.parse_args()

    dest_html = Path('output') / Path(args.conference + '.html')
    fetch_web_page(args.conference, dest_html)

    dest_json = Path('output') / Path(args.conference + '.json')
    if dest_json.is_file():
        with Path(dest_json).open(mode='r') as r:
            entries = json.load(r)
    else:
        entries = parse_html(dest_html)
        with Path(dest_json).open(mode='w') as w:
            json.dump(entries, w, ensure_ascii=False, indent=True)

    results = []
    for entry in tqdm(entries):
        title = entry['title']
        authors = entry.get('authors', [])
        arxiv_paper = search_arxiv(title, authors)
        if arxiv_paper is not None:
            results.append((title, authors, arxiv_paper))

    dest_csv = Path('output') / Path(args.conference + '.csv')
    dest_csv.parent.mkdir(parents=True, exist_ok=True)

    with dest_csv.open(mode='w') as w:
        HEADER = ['title in the list',
                  'authors in the list',
                  'url found',
                  'title found',
                  'authors found']
        writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(HEADER)
        for (title, authors, arxiv_paper) in results:
            str_authors = stringify_authors(authors)
            str_authors_found = stringify_authors(arxiv_paper.authors)
            writer.writerow([title,
                             str_authors,
                             arxiv_paper.uri,
                             'SAME TITLE' if same(title, arxiv_paper.title) else arxiv_paper.title,
                             'SAME AUTHORS' if same(str_authors, str_authors_found) else str_authors_found])


if __name__ == '__main__':
    main()
