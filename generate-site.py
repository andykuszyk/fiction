#!/usr/local/bin/python3
import sys
import os
import re
import logging

filename = sys.argv[1]
dirname = os.path.splitext(filename)[0]
if not os.path.exists(dirname):
    os.mkdir(dirname)

with open(filename, 'r') as f:
    lines = f.read().split('\n')

chapters = []
chapter = {}
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

print('Found {} chapters'.format(len(chapters)))
for chapter in chapters:
    print(chapter['title'])
    with open(os.path.join(dirname, '{}.html'.format(chapter['id'])), 'w') as f:
        f.write('<h1>{}</h1>\n'.format(chapter['title']))
        for line in chapter['lines']:
            f.write('{}\n'.format(line))
