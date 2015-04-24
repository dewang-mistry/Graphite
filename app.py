from flask import Flask, render_template, request, redirect
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

from tinydb import TinyDB, where
from slugify import slugify
import markdown2 as md
from unipath import Path
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
#db = TinyDB('notebooks.json')
db = TinyDB('meta-db.json')
notebooks_dir = Path('notebooks')
link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]

def get_html_from_md(md_text):
	return md.markdown(md_text, extras=["code-friendly", "fenced-code-blocks", "tables", "metadata", "cuddled-lists"])




@app.route('/', defaults={'notebook': None})
@app.route('/<notebook>', methods=['GET', 'POST'])
def index(notebook):
    #return '<h1>Hello World!</h1>'
    if notebook == None:
    	notebooks_list = db.all();
    	return render_template('index.html', notebooks=notebooks_list)
    else:
		if request.method == 'POST':
			# Check if the notebook already exists
			selected_notebook = db.search(where('slug') == notebook)
			notebook_data = {}

			if selected_notebook:
				notebook_data['title'] = selected_notebook[0].get('title')
				notebook_data['slug'] = selected_notebook[0].get('slig')
				notebook_data['desc'] = selected_notebook[0].get('desc')

				new_md_file = Path(notebooks_dir, notebook + '.md')
				new_md_file.write_file('\n'.join(request.form['content'].split('\r\n')))

				db.update({'desc':request.form['desc'], 'title':request.form['title']}, where('slug') == notebook)
			else:
				notebook_data['title'] = request.form['title']
				notebook_data['slug'] = slugify(request.form['title'])
				notebook_data['desc'] = request.form['desc']
				notebook_data['links'] = []
				#notebook_data['content'] = request.form['content'].split('\r\n')
				#Create markdown file under notebooks dir
				new_md_file = Path(notebooks_dir, notebook_data['slug'] + '.md')
				new_md_file.write_file('\n'.join(request.form['content'].split('\r\n')))

				db.insert(notebook_data)
				notebook = notebook_data['slug']

			#return render_template('notebook.html', notebook=notebook_data)
			return redirect(notebook)
		else:
			notebook_data = {}
			notebook_html = ''

			mode = request.args.get('m')
			selected_notebook = db.search(where('slug') == notebook)
			notebook_path = Path(notebooks_dir, notebook + '.md')
			
			if selected_notebook:
				notebook_data['title'] = selected_notebook[0].get('title')
				notebook_data['desc'] = selected_notebook[0].get('desc')
			else:
				notebook_data['title'] = ''
				notebook_data['desc'] = ''
				notebook_data['content'] = ''
				mode = 'edit'

			if mode == None:
				if selected_notebook:
					if notebook_path.exists():
						#notebook_html = md.markdown(notebook_path.read_file(), extras=["code-friendly", "fenced-code-blocks", "tables", "metadata", "cuddled-lists"])
						notebook_html = get_html_from_md(notebook_path.read_file())

						# Parse html using BeautifulSoup and extract all the links
						soup = BeautifulSoup(notebook_html, "lxml")
						print(soup.find_all('a'))

						notebook_data['content'] = notebook_html
					#notebook_data['content'] = '\n'.join(selected_notebook[0].get('content'))

				return render_template('notebook.html', notebook=notebook_data)
			else:
				if selected_notebook:
					if notebook_path.exists():
						notebook_html = notebook_path.read_file()
						notebook_data['content'] = notebook_html

				return render_template('notebook-edit.html', notebook=notebook_data)


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
