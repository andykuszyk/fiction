import os
import re
import shutil


PARAGRAPHS_PER_PART = 10


def make_title(d):
    title = d.replace('-', ' ')
    capitilise_next = True 
    capitalised_title = ''
    for i in range(0, len(title)):
        if capitilise_next:
            capitalised_title += title[i].capitalize()
        else:
            capitalised_title += title[i]
        capitilise_next = title[i] == ' '
    return capitalised_title


def get_dir(filename):
    dirname = os.path.splitext(filename)[0]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname


def read_lines(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def extract_paragraphs(lines):
    paragraphs = []
    for line in lines:
        if len(line) == 0 or line == '\n':
            paragraphs.append([])
        elif '<p>' in line and '</p>' in line:
            paragraphs.append([line])
        else:
            paragraphs[-1].append(line)
    return paragraphs


def build_parts(lines):
    parts = []
    paragraphs = extract_paragraphs(lines)
    print('Found {} paragraphs'.format(len(paragraphs)))
    if len(paragraphs) <= PARAGRAPHS_PER_PART:
        parts.append(paragraphs)
    else:
        start_index = 0
        while start_index + PARAGRAPHS_PER_PART < len(paragraphs):
            end_index = start_index + PARAGRAPHS_PER_PART
            parts.append(paragraphs[start_index:end_index])
            start_index += PARAGRAPHS_PER_PART
        parts.append(paragraphs[start_index:])
    print('Built {} parts'.format(len(parts)))
    return parts


def has_chapters(lines):
    for line in lines:
        if '<h1' in line:
            return True
    return False


def build_chapters(lines):
    chapters = []
    chapter = {}
    if not has_chapters(lines):
        chapter['title'] = ''
        chapter['id'] = ''
        chapter['lines'] = []
        chapters.append(chapter)
    for line in lines:
        if '<h1' in line:
            chapter = {}
            title_matches = re.search('>(.*)<', line)
            if len(title_matches.groups()) == 1:
                chapter['title'] = title_matches.groups()[0]
            else:
                logging.warn('malformed title, skipping: %s', line)
                continue
            id_matches = re.search('"(.*)"', line)
            if len(id_matches.groups()) == 1:
                chapter['id'] = id_matches.groups()[0]
            else:
                logging.warn('malformed id, skipping: %s', line)
                continue
            chapter['lines'] = []
            chapters.append(chapter)
        else:
            chapter['lines'].append(line)
    for chapter in chapters:
        chapter['parts'] = build_parts(chapter['lines'])

    for chapter in chapters:
        print('Parsing information for chapter {}:'.format(chapter['id']))
        print('{} parts:'.format(len(chapter['parts'])))
        for part in chapter['parts']:
            print('---> {} paragraphs;'.format(len(part)))
    return chapters



def downloads(filename, dirname):
    title = os.path.splitext(filename)[0]
    files = []
    for extension in ['pdf', 'epub']:
        download = '{}.{}'.format(title, extension)
        if os.path.exists(download):
            files.append(download)
            shutil.copyfile(download, os.path.join(dirname, download))
    print('Found downloads: {}'.format(files))
    return files

