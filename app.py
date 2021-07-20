from flask import Flask, url_for, request
from flask.templating import render_template
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect

import os
import glob
from random import randint

import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

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

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        #############
        # Suchanfrage
        #############
        keyword = request.form['keyword']
        area = request.form['area']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        speeches = Speeches.query.filter(Speeches.pdf.contains(keyword)).order_by(Speeches.date).limit(25).all()
        speeches_list = []
        for i in range(5):
            speeches_list.append([speeches[i:i+5]])
        print(speeches_list)
        textt = "empty empty empty results"
        for speech in speeches:
            textt = textt + speech.pdf
        #get all wordcloud images and delete them exept the default one
        all_wordclouds = glob.glob("static/images/wordcloud*")
        for path in all_wordclouds:
            if path == "static/images/wordcloud.png":
               continue
            os.remove(path)

        wordcloud = WordCloud().generate(textt)
        random_path = random_with_N_digits(5)
        new_wordcloud_path = "static/images/wordcloud" + str(random_path) + ".png"
        wordcloud.to_file(new_wordcloud_path)

        countries = [['Germany', 100, 20, 60], ['France', 90, 33, 80], ['Netherlands', 80, 25, 66]]
        img_paths = [new_wordcloud_path, new_wordcloud_path, new_wordcloud_path]

        return render_template('index.html', speeches = speeches, top_countries = countries, img_paths = img_paths)



    if request.method == 'GET':
        #####################
        # Normaler Seitenload
        #####################
        speeches = Speeches.query.order_by(Speeches.date).limit(10).all()
        textt = "empty empty empty results"
        for speech in speeches:
            textt = textt + speech.pdf
        #get all wordcloud images and delete them exept the default one
        all_wordclouds = glob.glob("static/images/wordcloud*")
        for path in all_wordclouds:
            if path == "static/images/wordcloud.png":
               continue
            os.remove(path)

        wordcloud = WordCloud().generate(textt)
        random_path = random_with_N_digits(5)
        new_wordcloud_path = "static/images/wordcloud" + str(random_path) + ".png"
        wordcloud.to_file(new_wordcloud_path)

        countries = [['Germany', 100, 20, 60], ['France', 90, 33, 80], ['Netherlands', 80, 25, 66]]
        img_paths = [new_wordcloud_path, new_wordcloud_path, new_wordcloud_path]

        return render_template('index.html', speeches = speeches, top_countries = countries, img_paths = img_paths)
    
        
    else:
        speeches = Speeches.query.order_by(Speeches.date).limit(10).all()
        return render_template('tour.html', speeches = speeches)
        #return render_template('index.html')

@app.route('/topicmodeling', methods=['POST', 'GET'])
def topicmodeling():
    if request.method == 'POST':
        pass

    else:
        return render_template('topicmodeling.html')

@app.route('/tour', methods=['POST', 'GET'])
def tour():
    if request.method == 'POST':
        pass

    else:
        return render_template('tour.html')

@app.route('/impressum', methods=['POST', 'GET'])
def impressum():
    if request.method == 'POST':
        pass

    else:
        return render_template('impressum.html')

if __name__ == "__main__":
    app.run(debug=True)