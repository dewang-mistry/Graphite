from flask import Flask, render_template, request
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/', defaults={'notebook': None})
@app.route('/<notebook>', methods=['GET', 'POST'])
def index(notebook):
    #return '<h1>Hello World!</h1>'
    if notebook == None:
    	notebooks = [];
    	notebooks.append({'name':'Designer', 'url':'designer', 'desc':'This is some notebook description. Maybe the first sentence.'})
    	notebooks.append({'name':'Developer', 'url':'developer', 'desc':'This is some notebook description. Maybe the first sentence.'})
    	notebooks.append({'name':'Data Scientist', 'url':'data-science', 'desc':'This is some notebook description. Maybe the first sentence.'})

    	return render_template('index.html', notebooks=notebooks)
    else:
		content = """On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."""
		if request.method == 'POST':
			#print(request.form['title'])
			#print(request.form['content'].split('\r\n'))
			return render_template('notebook.html', title=notebook, content=content)
		else:
			mode = request.args.get('m')

			if mode == None:
				return render_template('notebook.html', title=notebook, content=content)
			else:
				return render_template('notebook-edit.html', title=notebook, content=content)


@app.route('/notebook/<notebook_name>')
def notebook(notebook_name):
	return render_template('index.html', title=notebook_name, content=notebook_name)

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
