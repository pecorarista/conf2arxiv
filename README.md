conf2arxiv
==========

Search arXiv for papers accepted by specified conferences


## Requrements
Python 3.6+ is required.
The dependent modules are installed by
```sh
pip install -r requirements.txt
```

## Usage

```
usage: conf2arxiv [-h] json_path csv_dest

positional arguments:
  json_path   [{title: str, authors: [str]}]
  csv_dest    dest where the result is saved
```

For example
```sh
python -m conf2arxiv resource/example.json output/result.csv
```
