from flask import Flask, url_for, request
from flask.templating import render_template
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect

import matplotlib.pyplot as plt
import nltk
from wordloud import WordCloud

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bis_cb_speches_db_20_21.db'
db = SQLAlchemy(app)

class Speeches(db.Model):
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)
    

    def __repr__(self):
        return '<Speech %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        zug_name = request.form['name']
        speeches = Speeches.query.filter(Speeches.pdf.contains(zug_name)).order_by(Speeches.date).limit(10).all()
        textt = ""
        for speech in speeches:
            textt.join(speech.pdf)        
        wordcloud = WordCloud().generate(textt)
        return render_template('index.html', speeches = speeches)
        

        
    else:
        speeches = Speeches.query.order_by(Speeches.date).limit(10).all()
        return render_template('index.html', speeches = speeches)
        #return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)