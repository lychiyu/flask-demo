from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'index page'


@app.route('/hello')
def hello():
    name = 'hello world page'
    return render_template('hello.html', name=name)


@app.route('/profile/<username>')
def get_profile(username):
    return 'user %s' % username


@app.route('/get_post/<int:post_id>')
def get_post(post_id):
    return 'post_id %d' % post_id


if __name__ == '__main__':
    app.debug = True
    # app.run(debug=True, host='0.0.0.0',port='5000')
    app.run()
