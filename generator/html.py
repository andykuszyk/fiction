import os
from . import parsing

def write_index(dirname, chapters, title, filename):
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
            f.write('<a href="/{}/{}-1.html"><h3><li>{}</li></h3></a>\n'.format(dirname, chapter['id'], chapter['title']))
        f.write('''
                    </ol>
                </div>
                <div class="col-sm"></div>
            </div>
            <div class="row">
                <div class="col-lg">
                    <h2>Downloads</h2>
                    <hr>
                </div>
                <div class="col-sm"></div>
            </div>
            <div class="row">
                <div class="col-sm"></div>
                <div class="col-lg">''')
        f.write(download_links(parsing.downloads(filename, dirname)))
        f.write('''
                </div>
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


def comments_js(project_id):
    return '''
<script>
        loadComments = function() {
            $.get('/topics/'''+project_id+'''/comments', function(data) {
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
                    url: '/topics/'''+project_id+'''/comments',
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
            with open(os.path.join(dirname, '{}-{}.html'.format(chapter['id'], part_number)), 'w') as f:
                f.write('''
<!doctype html>
<html lang="en">
    <head>''')
                f.write(google_analytics())
                f.write('<title>A. Kuszyk | {} - {} ({}/{})</title>'.format(title, chapter['title'], part_number, len(chapter['parts'])))
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
                f.write('<h3>Part {}/{}\n'.format(part_number, len(chapter['parts'])))
                f.write('''
                <hr>
            </div>
            <div class="col-sm"></div>
        </div>
        <div class="row">
            <div class="col-sm"></div>
            <div class="col-lg">''')
                for paragraph in paragraphs:
                    for line in paragraph:
                        f.write(clean_line(line))
                f.write('''
                <hr>
                <p style="text-align:center">''')
                f.write(build_chapter_breadcrumb(chapter, part_index))
                f.write('<br><a href="{}">Previous Chapter</a> | <a href="{}">Next Chapter</a>'.format(previous_link, next_link))
                f.write('''
                </p>
            </div>
        </div>''')
                f.write(comments_markup())
                f.write(comments_js(project_id))
                f.write(''' 
    </div>
    </body>
</html>''')


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


