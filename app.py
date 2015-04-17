from flask import Flask, render_template
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    #return '<h1>Hello World!</h1>'
    content = """
    	On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.
    """
    return render_template('index.html', title='Hello World!', content=content)


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
