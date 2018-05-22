from unittest import TestCase

from conf2arxiv.search import search_arxiv


class TestSearch(TestCase):

    def test_search(self):
        title = 'Understanding Black-box Predictions via Influence Functions'
        authors = ['Pang Wei Koh', 'Percy Liang']
        arxiv_paper = search_arxiv(title, authors)
        self.assertEqual(title, arxiv_paper.title)
        self.assertEqual(authors[0].lower(),
                         arxiv_paper.authors[0].lower())
