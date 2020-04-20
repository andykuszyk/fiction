#!/usr/local/bin/python3
import sys
import os
import re
import logging

def makeTitle(d):
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

filename = sys.argv[1]
dirname = os.path.splitext(filename)[0]
title = makeTitle(dirname)
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
with open(os.path.join(dirname, 'index.html'), 'w') as f:
    f.write('''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    <body>
    <div class="container">
        <div class="row">
            <div class="col">''')
    f.write('<h1 class="display-1">{}</h1>\n'.format(title))
    f.write('''
                <ol>''')
    for chapter in chapters:
        f.write('<a href="/{}/{}.html"><h3><li>{}</li></h3></a>\n'.format(dirname, chapter['id'], chapter['title']))
    f.write('''
                </ol>
            </div>
        </div>
    </div>
    </body>
</html>''')

for i in range(0, len(chapters)):
    chapter = chapters[i]
    previous_link = '/{}'.format(dirname)
    if i > 0:
        previous_link = '/{}/{}.html'.format(dirname, chapters[i-1]['id'])
    next_link = '/{}'.format(dirname)
    if i < len(chapters) - 1:
        next_link = '/{}/{}.html'.format(dirname, chapters[i+1]['id'])

    print(chapter['title'])
    with open(os.path.join(dirname, '{}.html'.format(chapter['id'])), 'w') as f:
        f.write('''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    <body>
    <div class="container">
        <div class="row">
            <div class="col-lg">''')
        f.write('<h1>{}</h1>\n'.format(title))
        f.write('<h2>{}</h2>\n'.format(chapter['title']))
        f.write('''
            </div>
            <div class="col-sm"></div>
        </div>
        <div class="row">
            <div class="col-sm"></div>
            <div class="col-lg">''')
        for line in chapter['lines']:
            f.write('{}\n'.format(
                line
                    .replace('“', '"')
                    .replace('”', '"')
                    .replace('’', "'")
                    .replace('*', '<hr>')
            ))
        f.write('''
            <hr>
            <p style="text-align:center">''')
        f.write('<a href="{}">Previous</a>'.format(previous_link))
        f.write(' | ')
        f.write('<a href="{}">Next</a>'.format(next_link))
        f.write('''
                </p>
            </div>
        </div>
    </div>
    </body>
</html>''')
