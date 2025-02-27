from flask import Flask, render_template, g, redirect, request

app = Flask(__name__)

@app.before_request
def load_contents():
    with open('book_viewer/data/toc.txt', 'r') as file:
        g.contents = file.readlines()

def in_paragraphs(chapter_content):
    paragraphs = chapter_content.split('\n\n')
    result = ''
    for num, paragraph in enumerate(paragraphs, start=1):
        if paragraph:
            result += f'<p id="{num}">{paragraph}</p>'

    return result

app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.route("/")
def home():
    return render_template('home.html', contents=g.contents)

@app.route("/chapters/<page_num>")
def chapters(page_num):

    chapter_name = g.contents[int(page_num) - 1]
    chapter_title = f'Chapter {page_num}: {chapter_name}'

    with open(f'book_viewer/data/chp{page_num}.txt', 'r') as file:
        chapter_text = file.read()
    
    return render_template('chapter.html',
                           contents=g.contents,
                           chapter_title = chapter_title,
                           chapter_text = chapter_text)

def chapters_matching(query):
    if not query:
        return []
    
    matching_chapters = []
    for index, name in enumerate(g.contents, start=1):
        with open(f'book_viewer/data/chp{index}.txt', 'r') as file:
            chapter_contents = file.read()

        if query in chapter_contents:
            paragraphs = chapter_contents.split('\n\n')

            lst = []
            for paragraph in paragraphs:
                if query in paragraph:
                    lst.append(paragraph)

            matching_chapters.append({'number': index, 'name': name, 'paragraphs': lst})
    
    return matching_chapters

@app.route("/search")
def search():
    query = request.args.get('query', '')
    results = chapters_matching(query)
    return render_template('search.html', query=query, results=results)

@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5003)