from flask import Flask, url_for, request
from flask.templating import render_template
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect

import os
import glob
from random import randint
import math
from collections import Counter

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


def pagination(speeches):
    speeches_list = []
    for i in range(math.ceil(len(speeches)/5)):
        ifive = i*5
        speeches_list.append(speeches[ifive:ifive+5])
    return speeches_list


def delete_old_wordclouds():
    all_wordclouds = glob.glob("static/images/wordcloud*")
    for path in all_wordclouds:
        os.remove(path)


def create_new_wordCloud(speeches):

    delete_old_wordclouds()
    textt = "empty empty empty results"
    for speech in speeches:
        textt = textt + speech.pdf

    wordcloud = WordCloud().generate(textt)
    random_path = random_with_N_digits(5)
    new_wordcloud_path = "static/images/wordcloud" + str(random_path) + ".png"
    wordcloud.to_file(new_wordcloud_path)
    return new_wordcloud_path


def delete_old_timelines():
    all_timelines = glob.glob("static/images/timeline*")
    for path in all_timelines:
        os.remove(path)


def create_new_timeline(speeches, keyword):
    # delete old timelines
    delete_old_timelines()
    plt.clf()
    # loop through speeches and get count of keyword    
    keys = []
    values = []
    for speech in speeches:
        # add the date of the speech and the count of hits
        keys.append(datetime.fromtimestamp(speech.date))
        values.append(speech.pdf.upper().count(keyword.upper()))

    random_path = random_with_N_digits(5)
    new_timeline_path = "static/images/timeline" + str(random_path) + ".png"
    plt.style.use("dark_background")
    plt.scatter(keys, values)    
    
    plt.savefig(new_timeline_path, bbox_inches='tight')
    
    return new_timeline_path

    # there is the data

# Date filter


@app.template_filter('datefromint')
def format_date(int):
    date = datetime.fromtimestamp(int)
    date_formatted = date.strftime('%d.%m.%Y')
    return date_formatted


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

        speeches = Speeches.query.filter(Speeches.pdf.contains(
            keyword)).order_by(Speeches.date).limit(25).all()

        speeches_list = pagination(speeches)
        frequencies = create_new_timeline(speeches, keyword)

        new_wordcloud_path = create_new_wordCloud(speeches)
        new_timeline_path = create_new_timeline(speeches, keyword)

        countries = [['Germany', 100, 20, 60], [
            'France', 90, 33, 80], ['Netherlands', 80, 25, 66]]
        img_paths = [new_wordcloud_path,
                     new_timeline_path, new_wordcloud_path]

        return render_template('index.html', speeches_count=len(speeches), speeches=speeches_list, top_countries=countries, img_paths=img_paths, frequencies = frequencies)

    if request.method == 'GET':
        #####################
        # Normaler Seitenload
        #####################
        speeches = Speeches.query.order_by(Speeches.date).limit(25).all()
        speeches_list = pagination(speeches)

        new_wordcloud_path = create_new_wordCloud(speeches)

        frequencies = create_new_timeline(speeches, "Bitcoin")

        countries = [['Germany', 100, 20, 60], [
            'France', 90, 33, 80], ['Netherlands', 80, 25, 66]]
        img_paths = [new_wordcloud_path,
                     new_wordcloud_path, new_wordcloud_path]

        return render_template('index.html', speeches=speeches_list, top_countries=countries, img_paths=img_paths, frequencies = frequencies)

    else:
        speeches = Speeches.query.order_by(Speeches.date).limit(10).all()
        return render_template('tour.html', speeches=speeches)
        # return render_template('index.html')


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
