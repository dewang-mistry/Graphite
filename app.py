from flask import Flask, render_template, request, redirect
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap
from tinydb import TinyDB, where
from slugify import slugify
from flaskext.markdown import Markdown

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
db = TinyDB('notebooks.json')
Markdown(app)

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
				notebook_data['content'] = '\n'.join(selected_notebook[0].get('content'))

				db.update({'content': request.form['content'].split('\r\n'), 'desc':request.form['desc'], 'title':request.form['title']}, where('slug') == notebook)
			else:
				notebook_data['title'] = request.form['title']
				notebook_data['slug'] = slugify(request.form['title'])
				notebook_data['desc'] = request.form['desc']
				notebook_data['content'] = request.form['content'].split('\r\n')

				db.insert(notebook_data)

			#return render_template('notebook.html', notebook=notebook_data)
			return redirect(notebook)
		else:
			notebook_data = {}
			mode = request.args.get('m')
			selected_notebook = db.search(where('slug') == notebook)
			
			if selected_notebook:
				notebook_data['title'] = selected_notebook[0].get('title')
				notebook_data['desc'] = selected_notebook[0].get('desc')
			else:
				notebook_data['title'] = ''
				notebook_data['desc'] = ''
				notebook_data['content'] = ''

			if mode == None:
				if selected_notebook:
					notebook_data['content'] = '\n'.join(selected_notebook[0].get('content'))

				return render_template('notebook.html', notebook=notebook_data)
			else:
				if selected_notebook:
					notebook_data['content'] = '\r\n'.join(selected_notebook[0].get('content'))

				return render_template('notebook-edit.html', notebook=notebook_data)

@app.route('/notebook/<notebook_name>')
def notebook(notebook_name):
	return render_template('index.html', title=notebook_name, content=notebook_name)

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
