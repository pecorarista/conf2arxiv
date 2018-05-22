from typing import List


def stringify_authors(authors: List[str]) -> str:
    if len(authors) == 0:
        return ''
    elif len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return authors[0] + ' and ' + authors[1]
    elif len(authors) > 2:
        return ', '.join(authors[:-1]) + ', and ' + authors[-1]
