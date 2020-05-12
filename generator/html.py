import os
from . import parsing


def read_template(name):
    with open('./generator/templates/{}.html'.format(name), 'r') as f:
        return f.read()


def write_short(title, dirname, chapters, filename, project_id):
    short_html = read_template('chapter')
    short_html = short_html.replace('%TITLE%', title)
    heading = '<h1>{}</h1>\n{}'.format(title, download_links(parsing.downloads(filename, dirname)))
    short_html = short_html.replace('%HEADING%', heading)
    lines = ''
    for chapter in chapters:
        lines += '<h2>{}</h2>\n'.format(chapter['title'])
        for line in chapter['lines']:
            lines += clean_line(line)
        lines += '<hr>'
    short_html = short_html.replace('%LINES%', lines)
    short_html = short_html.replace('%BREADCRUMB%', '')
    short_html = short_html.replace('%CHAPTER_LINKS%', '')
    short_html = short_html.replace('%PROJECT_ID%', project_id)
    with open(os.path.join(dirname, 'index.html'), 'w') as f:
        f.write(short_html)


def write_index(dirname, chapters, title, filename):
    print('Found {} chapters'.format(len(chapters)))
    index_html = read_template("index")
    index_html = index_html.replace('%TITLE%', title)
    chapter_links = ''
    for chapter in chapters:
        chapter_links += '<a href="/{}/{}-1.html"><h3><li>{}</li></h3></a>\n'.format(dirname, chapter['id'], chapter['title'])
    index_html = index_html.replace('%CHAPTER_LINKS%', chapter_links)
    index_html = index_html.replace('%DOWNLOAD_LINKS%', download_links(parsing.downloads(filename, dirname)))
    with open(os.path.join(dirname, 'index.html'), 'w') as f:
        f.write(index_html)


def clean_line(line):
    return '{}\n'.format(line
        .replace('“', '"')
        .replace('”', '"')
        .replace('’', "'")
        .replace('*', '<hr>')
    )


def build_chapter_breadcrumb(chapter, part_index):
    breadcrumb = '|'
    for i in range(0, len(chapter['parts'])):
        if i == part_index:
            breadcrumb += ' {} |'.format(part_index + 1)
        else:
            breadcrumb += ' <a href="{}-{}.html">{}</a> |'.format(chapter['id'], i + 1, i + 1)
    return breadcrumb


def write_chapters(title, dirname, chapters, project_id):
    for i in range(0, len(chapters)):
        chapter = chapters[i]
        previous_link = '/{}'.format(dirname)
        if i > 0:
            previous_link = '/{}/{}-1.html'.format(dirname, chapters[i-1]['id'])
        next_link = '/{}'.format(dirname)
        if i < len(chapters) - 1:
            next_link = '/{}/{}-1.html'.format(dirname, chapters[i+1]['id'])

        print(chapter['title'])
        for part_index in range(0, len(chapter['parts'])):
            paragraphs = chapter['parts'][part_index]
            part_number = part_index + 1
            chapter_html = read_template('chapter')
            chapter_html = chapter_html.replace('%TITLE%', '{} - {} ({}/{})'.format(title, chapter['title'], part_number, len(chapter['parts'])))
            heading = ''
            heading += '<h1>{}</h1>\n'.format(title)
            heading += '<h2>{}</h2>\n'.format(chapter['title'])
            heading += '<h3>Part {}/{}\n'.format(part_number, len(chapter['parts']))
            chapter_html = chapter_html.replace('%HEADING%', heading)
            lines = ''
            for paragraph in paragraphs:
                for line in paragraph:
                    lines += clean_line(line)
            chapter_html = chapter_html.replace('%LINES%', lines)
            chapter_html = chapter_html.replace('%BREADCRUMB%', build_chapter_breadcrumb(chapter, part_index))
            chapter_links = '<a href="{}">Previous Chapter</a> | <a href="{}">Next Chapter</a>'.format(previous_link, next_link)
            chapter_html = chapter_html.replace('%CHAPTER_LINKS%', chapter_links)
            chapter_html = chapter_html.replace('%PROJECT_ID%', project_id)

            with open(os.path.join(dirname, '{}-{}.html'.format(chapter['id'], part_number)), 'w') as f:
                f.write(chapter_html)


def download_links(download_files):
    if len(download_files) == 0:
        return ''
    links = '<h3>'
    for download in download_files:
        links += '<a href="{}">{}</a>  |  '.format(download, get_download_name(download))
    return '{}</h3>'.format(links[:-4])


def get_download_name(download):
    if 'pdf' in download:
        return 'PDF'
    elif 'epub' in download:
        return 'EPUB'
    else:
        return ''
