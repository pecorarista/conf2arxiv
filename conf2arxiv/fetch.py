from pathlib import Path
import requests


def fetch_web_page(conf: str, dest: Path) -> None:

    if dest.is_file():
        return
    if conf == 'acl2018':
        url = 'https://acl2018.org/programme/papers/'
    else:
        # TODO
        url = 'https://acl2018.org/programme/papers/'

    response = requests.get(url)
    with dest.open(mode='w') as w:
        w.write(response.text)
