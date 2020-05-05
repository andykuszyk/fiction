import unittest
from .. import parsing


class TestParsing(unittest.TestCase):

    def test_make_title(self):
        expected = 'Title Of Book'
        actual = parsing.make_title('title-of-book')
        self.assertEqual(expected, actual)
    
    def test_extract_paragraphs(self):
        lines = [ 
            '<p>this is some text, all in one</p>',
            '<p>this is some more text, in yet another</p>',
        ]
        paragraphs = parsing.extract_paragraphs(lines)
        self.assertEqual(len(paragraphs), 2)

    def test_build_chapters(self):
        lines = [
            '<h1 id="chapter-1">Chapter 1</h1>',
            '<p>paragraph</p>',
            '<p>paragraph</p>',
            '<p>paragraph</p>',
            '<p>paragraph</p>',
        ]
        parsing.PARAGRAPHS_PER_PART = 2
        chapters = parsing.build_chapters(lines)
        self.assertEqual(1, len(chapters))
        self.assertEqual(2, len(chapters[0]['parts']))
        self.assertEqual(2, len(chapters[0]['parts'][0]))
        self.assertEqual(2, len(chapters[0]['parts'][1]))

if __name__ == '__main__':
    unittest.main()
