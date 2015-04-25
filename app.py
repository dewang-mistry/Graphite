from flask import Flask, render_template, request, redirect, Response
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

from tinydb import TinyDB, where
from slugify import slugify
import markdown2 as md
from unipath import Path
import re
from bs4 import BeautifulSoup
import json
from purl import URL

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
#db = TinyDB('notebooks.json')
db = TinyDB('meta-db.json')
notebooks_dir = Path('notebooks')
link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]

def get_html_from_md(md_text):
	return md.markdown(md_text, extras=["code-friendly", "fenced-code-blocks", "tables", "metadata", "cuddled-lists"])

def get_all_links(html):
	links_array = []

	# Parse html using BeautifulSoup and extract all the links
	#soup = BeautifulSoup(html, "lxml")
	soup = BeautifulSoup(html)

	for link in soup.find_all('a'):
		links_array.append({'name':link.get_text(), 'url':link.get('href')})

	print(links_array)
	return links_array


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

				cleaned_md = '\n'.join(request.form['content'].split('\r\n'))
				notebook_data['links'] = get_all_links(get_html_from_md(cleaned_md))

				new_md_file.write_file(cleaned_md)
				db.update({'desc':request.form['desc'], 'title':request.form['title'], 'links':notebook_data['links']}, where('slug') == notebook)
			else:
				notebook_data['title'] = request.form['title']
				notebook_data['slug'] = slugify(request.form['title'])
				notebook_data['desc'] = request.form['desc']

				#notebook_data['content'] = request.form['content'].split('\r\n')
				#Create markdown file under notebooks dir
				new_md_file = Path(notebooks_dir, notebook_data['slug'] + '.md')
				cleaned_md = '\n'.join(request.form['content'].split('\r\n'))
				notebook_data['links'] = get_all_links(get_html_from_md(cleaned_md))

				new_md_file.write_file(cleaned_md)
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

						

						notebook_data['content'] = notebook_html
					#notebook_data['content'] = '\n'.join(selected_notebook[0].get('content'))

				return render_template('notebook.html', notebook=notebook_data)
			else:
				if selected_notebook:
					if notebook_path.exists():
						notebook_html = notebook_path.read_file()
						notebook_data['content'] = notebook_html

				return render_template('notebook-edit.html', notebook=notebook_data)

@app.route('/api/graph')
def graph():
	#nodes = [{'id':'notebook1', 'label':'Notebook 1'}, {'id':'notebook2', 'label':'Notebook 2'}]
	#edges = [{'from':'notebook1', 'to':'notebook2'}]
	nodes_map = {}
	nodes = []
	edges = []
	internal_link_color = '#0088d7'
	external_link_color = '#e70081'
	color = internal_link_color

	notebooks_list = db.all();

	if notebooks_list:
		for notebook in notebooks_list:
			# Create notebook nodes
			nodes_map.setdefault(notebook.get('slug'), notebook.get('title'))
			#nodes.append({'id':notebook.get('slug'), 'label':notebook.get('title')})

			# Get all links to create edges
			links = notebook.get('links')
			if links:
				for link in links:
					print(link)
					nodes_map.setdefault(link.get('url'), link.get('name'))
					edges.append({'from':notebook.get('slug'), 'to':link.get('url'), 'style':'arrow'})
					#nodes.append({'id':link.get('url'), 'label':link.get('name')})

		for url, name in nodes_map.iteritems():
			parsed_url = URL(url)

			if len(parsed_url.host()) > 0:
				nodes.append({'id':url, 'label':name, 'color':external_link_color})
			else:
				nodes.append({'id':url, 'label':name, 'color':internal_link_color})

	graph = {'nodes':nodes, 'edges':edges}

	return Response(json.dumps(graph), mimetype='text/json')


@app.route('/api/notebookList')
def notebook_list():
	names = []

	notebooks_list = db.all();

	if notebooks_list:
		for notebook in notebooks_list:
			names.append(notebook.get('title'))			


	return Response(json.dumps(names), mimetype='text/json')

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
