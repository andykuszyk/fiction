#!/usr/bin/python3
import sys
import os
import re
import logging


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


def get_chapters(lines):
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
    return chapters


def google_analytics():
    return '''
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-164357380-1"></script>
<script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-164357380-1');
</script>
    '''


def bootstrap():
    return '''
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">        
    '''


def write_index(dirname, chapters):
    print('Found {} chapters'.format(len(chapters)))
    with open(os.path.join(dirname, 'index.html'), 'w') as f:
        f.write('''
    <!doctype html>
    <html lang="en">
        <head>''')
        f.write(google_analytics())
        f.write('<title>A. Kuszyk | {}</title>'.format(title))
        f.write(bootstrap())
        f.write('''
         </head>
        <body>
        <div class="container">
            <div class="row">
                <div class="col-lg">''')
        f.write('<h1>{}</h1>\n'.format(title))
        f.write('''
                    <h2>Chapters</h2>
                    <hr>
                </div>
                <div class="col-sm"></div>
            </div>
            <div class="row">
                <div class="col-sm"></div>
                <div class="col-lg">
                    <ol>''')
        for chapter in chapters:
            f.write('<a href="/{}/{}.html"><h3><li>{}</li></h3></a>\n'.format(dirname, chapter['id'], chapter['title']))
        f.write('''
                    </ol>
                </div>
                <div class="col-sm"></div>
            </div>
        </div>
        </body>
    </html>''')


def timeline_css():
    return '''
<style>
    ul.timeline {
        list-style-type: none;
        position: relative;
    }
    ul.timeline:before {
        content: ' ';
        background: #d4d9df;
        display: inline-block;
        position: absolute;
        left: 29px;
        width: 2px;
        height: 100%;
        z-index: 400;
    }
    ul.timeline > li {
        margin: 20px 0;
        padding-left: 20px;
    }
    ul.timeline > li:before {
        content: ' ';
        background: white;
        display: inline-block;
        position: absolute;
        border-radius: 50%;
        border: 3px solid #22c0e8;
        left: 20px;
        width: 20px;
        height: 20px;
        z-index: 400;
    }
</style>
    '''


def clean_line(line):
    return '{}\n'.format(line
        .replace('“', '"')
        .replace('”', '"')
        .replace('’', "'")
        .replace('*', '<hr>')
    )


def comments_markup():
    return '''
<div id="app" class="row">
    <div class="col-md-6 offset-md-3">
        <h4>Comments</h4>
        <ul class="timeline">
            <li>
                <form>
                    <div class="form-group">
                        <label for="commentInput">All comments are welcome, especially constructive ones!</label>
                        <textarea v-model="newComment" class="form-control" id="commentInput" rows="3"></textarea>
                        <button type="button" class="btn btn-primary" v-on:click="submitComment">Submit</button>
                    </div>
                </form>
            </li>
            <li v-for="comment in comments">
                <p><b>{{ comment.createdAt }}</b></p>
                <p>{{ comment.body }}</p>
            </li>
        </ul>
    </div>
</div>
    '''


def comments_js():
    return '''
<script>
        loadComments = function() {
            $.get('/topics/16275216/comments', function(data) {
                console.log(typeof(data))
                comments = []
                for(d of data) {
                    createdAt = new Date(d.CreatedAt)
                    comments.push({createdAt: `${createdAt.toLocaleString()}`, body: d.Body})
                }
                app.$data.comments = comments
            })
        }

        var app = new Vue({
            el: '#app',
            data: {
                newComment: '',
                comments: []
            },
            methods: {
                submitComment: function() {
                console.log(app.newComment)
                $.post({
                    url: '/topics/16275216/comments',
                    data: JSON.stringify({Body: app.newComment}), 
                    contentType: 'application/json'
                }, function() {
                    loadComments()
                    app.newComment = ''
                })
            }
        }
    })

   loadComments() 
</script>
'''

def write_chapters(title, dirname, chapters):
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
<!doctype html>
<html lang="en">
    <head>''')
            f.write(google_analytics())
            f.write('<title>A. Kuszyk | {} - {}</title>'.format(title, chapter['title']))
            f.write(bootstrap())
            f.write('''
            <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>''')
            f.write(timeline_css())
            f.write('''
    </head>
    <body>
    <div class="container">
        <div class="row">
            <div class="col-lg">''')
            f.write('<h1>{}</h1>\n'.format(title))
            f.write('<h2>{}</h2>\n'.format(chapter['title']))
            f.write('''
                <hr>
            </div>
            <div class="col-sm"></div>
        </div>
        <div class="row">
            <div class="col-sm"></div>
            <div class="col-lg">''')
            for line in chapter['lines']:
                f.write(clean_line(line))
            f.write('''
                <hr>
                <p style="text-align:center">''')
            f.write('<a href="{}">Previous</a> | <a href="{}">Next</a>'.format(previous_link, next_link))
            f.write('''
                </p>
            </div>
        </div>''')
            f.write(comments_markup())
            f.write(comments_js())
            f.write(''' 
    </div>
    </body>
</html>''')


if __name__ == '__main__':
    filename = sys.argv[1]
    dirname = get_dir(filename) 
    title = make_title(dirname)
    lines = read_lines(filename)
    chapters = get_chapters(lines)

    write_index(dirname, chapters)
    write_chapters(title, dirname, chapters)
