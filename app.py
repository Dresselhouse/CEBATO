from flask import Flask, url_for, request
from flask.templating import render_template
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.utils import redirect

import os
import glob
from random import randint
import math
from collections import Counter

import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

# world map
from pycountry_convert import country_name_to_country_alpha2
import pygal
from pygal.style import DarkStyle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bis_cb_speches_db_20_21.db'
app.config['SQLALCHEMY_BINDS'] = {
        "db2010": "sqlite:///bis_cb_speches_db_2010.db",
        "db2011": "sqlite:///bis_cb_speches_db_2011.db",
        "db2012": "sqlite:///bis_cb_speches_db_2012.db",
        "db2013": "sqlite:///bis_cb_speches_db_2013.db",
        "db2014": "sqlite:///bis_cb_speches_db_2014.db",
        "db2015": "sqlite:///bis_cb_speches_db_2015.db",
        "db2016": "sqlite:///bis_cb_speches_db_2016.db"}
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

class Speeches2010(db.Model):
    __bind_key__ = "db2010"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2011(db.Model):
    __bind_key__ = "db2011"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2012(db.Model):
    __bind_key__ = "db2012"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2013(db.Model):
    __bind_key__ = "db2013"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2014(db.Model):
    __bind_key__ = "db2014"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2015(db.Model):
    __bind_key__ = "db2015"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id


class Speeches2016(db.Model):
    __bind_key__ = "db2016"
    
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


def prepare_map_data(speeches, keyword):
    data = {}
    for speech in speeches:
        try:
            cn_a2_code = country_name_to_country_alpha2(speech.title).lower()
        except:
            cn_a2_code = 'Unknown'
        # if this country already exists in the list the current hitcount gets added to the value
        # if not it becomes a new entry
        if cn_a2_code in data:
            data[cn_a2_code] += speech.pdf.upper().count(keyword.upper())
        else:
            data[cn_a2_code] = speech.pdf.upper().count(keyword.upper())

    return data


def delete_old_worldmaps():
    all_worldmaps = glob.glob("static/images/worldmap*")
    for path in all_worldmaps:
        os.remove(path)


def create_new_worldmaps(speeches, keyword):
    delete_old_worldmaps()
    # clear matplot from previous data
    plt.clf()

    data = prepare_map_data(speeches, keyword)
    # empty map

    # pygal map
    worldmap = pygal.maps.world.World(style=DarkStyle)
    worldmap.show_legend = False

    worldmap.title = 'Countries'
    worldmap.add('Frequencies', data)

    random_path = random_with_N_digits(5)
    new_worldmap_path = "static/images/worldmap" + str(random_path) + ".svg"
    worldmap.render_to_file(new_worldmap_path)
    return new_worldmap_path

def query_database(keyword, area, start, end):

    try: 
        start = datetime.fromisoformat(start).timestamp()   
    except:
        start = (datetime.utcnow() - timedelta(days=30)).timestamp()

    try:
        end = datetime.fromisoformat(end).timestamp()
    except:
        end = datetime.utcnow().timestamp()


    speeches = []

    if not start > 1293750000 or end < 1263337200:
        speeches.extend(Speeches2010.query.filter(Speeches2010.pdf.contains(
            keyword)).filter(Speeches2010.date > start).filter(Speeches2010.date < end).order_by(Speeches2010.date).limit(500).all())

    if not start > 1325199600 or end < 1294095600:
        speeches.extend(Speeches2011.query.filter(Speeches2011.pdf.contains(
            keyword)).filter(Speeches2011.date > start).filter(Speeches2011.date < end).order_by(Speeches2011.date).limit(500).all())

    if not start > 1355958000 or end < 1325458800:
        speeches.extend(Speeches2012.query.filter(Speeches2012.pdf.contains(
            keyword)).filter(Speeches2012.date > start).filter(Speeches2012.date < end).order_by(Speeches2012.date).limit(500).all())

    if not start > 1388444400 or end < 1357167600:
        speeches.extend(Speeches2013.query.filter(Speeches2013.pdf.contains(
            keyword)).filter(Speeches2013.date > start).filter(Speeches2013.date < end).order_by(Speeches2013.date).limit(500).all())

    if not start > 1418598000 or end < 1388962800:
        speeches.extend(Speeches2014.query.filter(Speeches2014.pdf.contains(
            keyword)).filter(Speeches2014.date > start).filter(Speeches2014.date < end).order_by(Speeches2014.date).limit(500).all())

    if not start > 1451430000 or end < 1420758000:
        speeches.extend(Speeches2015.query.filter(Speeches2015.pdf.contains(
            keyword)).filter(Speeches2015.date > start).filter(Speeches2015.date < end).order_by(Speeches2015.date).limit(500).all())

    if not start > 1475186400 or end < 1452466800:
        speeches.extend(Speeches2016.query.filter(Speeches2016.pdf.contains(
            keyword)).filter(Speeches2016.date > start).filter(Speeches2016.date < end).order_by(Speeches2016.date).limit(500).all())

    speeches.extend((Speeches.query.filter(Speeches.pdf.contains(
            keyword)).filter(Speeches.date > start).filter(Speeches.date < end).order_by(Speeches.date).limit(500).all()))

    return speeches

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

        speeches = query_database(keyword, area, startdate, enddate)

        speeches_list = pagination(speeches)
        frequencies = create_new_timeline(speeches, keyword)

        new_wordcloud_path = create_new_wordCloud(speeches)
        new_timeline_path = create_new_timeline(speeches, keyword)
        new_worldmap_path = create_new_worldmaps(speeches, keyword)

        countries = [['Germany', 100, 20, 60], [
            'France', 90, 33, 80], ['Netherlands', 80, 25, 66]]
        img_paths = [new_wordcloud_path,
                     new_timeline_path, new_worldmap_path]

        return render_template('index.html', speeches_count=len(speeches), speeches=speeches_list, top_countries=countries, img_paths=img_paths, frequencies=frequencies)

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

        return render_template('index.html', speeches=speeches_list, top_countries=countries, img_paths=img_paths, frequencies=frequencies)

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
