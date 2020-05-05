import sys
from . import parsing
from . import html

if __name__ == '__main__':
    filename = sys.argv[1]
    dirname = parsing.get_dir(filename) 
    title = parsing.make_title(dirname)
    lines = parsing.read_lines(filename)
    chapters = parsing.build_chapters(lines)

    html.write_index(dirname, chapters, title, filename)
    html.write_chapters(title, dirname, chapters)
