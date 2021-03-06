# Flask Web-Framework
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

# Standard Imports
from datetime import datetime, timedelta
import os
import glob
from random import randint, random
import math
import random

# Plots
import matplotlib.pyplot as plt

# Wordcloud
from wordcloud import WordCloud

# World Map
from pycountry_convert import country_name_to_country_alpha2
import pygal
from pygal.style import DarkStyle

#Natural Language Processing
import spacy
nlp = spacy.load('en_core_web_sm')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


################
# Config-Limits 
# (prevent server shutdowns. Can be set to high numbers when running local)
#################

kws_speeches_max = 200
lda_speeches_max = 50



# Initializing the app and databases
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bis_cb_speches_db_20_21.db'
app.config['SQLALCHEMY_BINDS'] = {
        "db2010": "sqlite:///bis_cb_speeches_db_10_clean.db",
        "db2011": "sqlite:///bis_cb_speeches_db_11_clean.db",
        "db2012": "sqlite:///bis_cb_speeches_db_12_clean.db",
        "db2013": "sqlite:///bis_cb_speeches_db_13_clean.db",
        "db2014": "sqlite:///bis_cb_speeches_db_14_clean.db",
        "db2015": "sqlite:///bis_cb_speeches_db_15_clean.db",
        "db2016": "sqlite:///bis_cb_speeches_db_16_clean.db",
        "db2017": "sqlite:///bis_cb_speeches_db_17_clean.db",
        "db2018": "sqlite:///bis_cb_speeches_db_18_clean.db",
        "db2019": "sqlite:///bis_cb_speeches_db_19_clean.db",
        "db2020": "sqlite:///bis_cb_speeches_db_20_clean.db",
        "db2021": "sqlite:///bis_cb_speeches_db_21_clean.db"}
db = SQLAlchemy(app)


#####################################
# Database Models for different years
#####################################

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

class Speeches2017(db.Model):
    __bind_key__ = "db2017"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2018(db.Model):
    __bind_key__ = "db2018"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2019(db.Model):
    __bind_key__ = "db2019"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2020(db.Model):
    __bind_key__ = "db2020"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id

class Speeches2021(db.Model):
    __bind_key__ = "db2021"
    
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Integer)
    author = db.Column(db.String)
    country = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.String)

    def __repr__(self):
        return '<Speech %r>' % self.id


##########################
# Custom defined functions
##########################

def random_with_N_digits(n):
    # Used for randomized Image Paths to prevent browsers from showing old, cached plots
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def pagination(speeches):

    # Seperating the list of speeches from the search to chunks

    if len(speeches) > 25:
        speeches = speeches[0:25]

    speeches_list = []
    for i in range(math.ceil(len(speeches)/5)):
        ifive = i*5
        speeches_list.append(speeches[ifive:ifive+5])
    return speeches_list


def delete_old_wordclouds():
    # Search for all old worldclouds and delete them

    all_wordclouds = glob.glob("static/images/wordcloud*")
    for path in all_wordclouds:
        os.remove(path)


def create_new_wordCloud(speeches):
    # Generates a new wordcloud from a list of speeches, returns the file path

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
    # Searches for all old timelines and deletes them

    all_timelines = glob.glob("static/images/timeline*")
    for path in all_timelines:
        os.remove(path)


def create_new_timeline(speeches, keyword):
    # delete old timelines
    delete_old_timelines()
    plt.clf()
    # Prepares the data for the plot
    keys = []
    values = []
    for speech in speeches:
        # add the date of the speech and the count of hits
        keys.append(datetime.fromtimestamp(speech.date))
        values.append(speech.pdf.upper().count(keyword.upper()))

    # Plot creation and export
    random_path = random_with_N_digits(5)
    new_timeline_path = "static/images/timeline" + str(random_path) + ".png"
    plt.style.use("dark_background")
    plt.scatter(keys, values)
    plt.savefig(new_timeline_path, bbox_inches='tight')

    return new_timeline_path


def prepare_map_data(speeches, keyword):
    # Counts the number of hits for every speech and every country

    data = {}
    data_alpha = {}
    for speech in speeches:

        # if this country already exists in the list the current hitcount gets added to the value
        # if not it becomes a new entry
        # 1 gets added to the speech count

        if speech.country in data:
            data[speech.country][0] += speech.pdf.upper().count(keyword.upper())
            data[speech.country][1] += 1
        else:
            data[speech.country] = [0, 0]
            data[speech.country][0] += speech.pdf.upper().count(keyword.upper())
            data[speech.country][1] += 1

    for country in data:
        # Try to convert the country name into the Alpha2-Code
        # If it is successfull the country and its hit code gets added to the list
        # This list gets later passed to the Pygal Package to create the world map
        # The other list is used for the display of the top 3 countries

        try:
            cn_a2_code = country_name_to_country_alpha2(country).lower() 
            data_alpha[cn_a2_code] = data[country][1]
        except:
            cn_a2_code = 'Unknown'
         

    return data, data_alpha


def delete_old_worldmaps():
    # Search for old worldmaps and delete them

    all_worldmaps = glob.glob("static/images/worldmap*")
    for path in all_worldmaps:
        os.remove(path)


def create_new_worldmaps(speeches, keyword):

    delete_old_worldmaps()

    # clear matplot from previous data
    plt.clf()

    # Call Data-Prep-Function and save the results
    dataDicts = prepare_map_data(speeches, keyword)
    data = dataDicts[1]
    top_countries = [(k, dataDicts[0][k]) for k in sorted(dataDicts[0], key=dataDicts[0].get, reverse=True)][0:3]
    
    # Create Pygal Map
    worldmap = pygal.maps.world.World(style=DarkStyle)
    worldmap.show_legend = False

    # Add the data to the map
    worldmap.title = 'Countries'
    worldmap.add('Frequencies', data)

    # Export as vector image
    random_path = random_with_N_digits(5)
    new_worldmap_path = "static/images/worldmap" + str(random_path) + ".svg"
    worldmap.render_to_file(new_worldmap_path)    

    return new_worldmap_path, top_countries
    

def query_database_all_area(keyword, area, start, end):

    speeches = []

    if not start > 1293750000 or end < 1263337200:
        speeches.extend(Speeches2010.query.filter(Speeches2010.pdf.contains(
            keyword)).filter(Speeches2010.date > start).filter(Speeches2010.date < end).order_by(Speeches2010.date).all())

    if not start > 1325199600 or end < 1294095600:
        speeches.extend(Speeches2011.query.filter(Speeches2011.pdf.contains(
            keyword)).filter(Speeches2011.date > start).filter(Speeches2011.date < end).order_by(Speeches2011.date).all())

    if not start > 1355958000 or end < 1325458800:
        speeches.extend(Speeches2012.query.filter(Speeches2012.pdf.contains(
            keyword)).filter(Speeches2012.date > start).filter(Speeches2012.date < end).order_by(Speeches2012.date).all())

    if not start > 1388444400 or end < 1357167600:
        speeches.extend(Speeches2013.query.filter(Speeches2013.pdf.contains(
            keyword)).filter(Speeches2013.date > start).filter(Speeches2013.date < end).order_by(Speeches2013.date).all())

    if not start > 1418598000 or end < 1388962800:
        speeches.extend(Speeches2014.query.filter(Speeches2014.pdf.contains(
            keyword)).filter(Speeches2014.date > start).filter(Speeches2014.date < end).order_by(Speeches2014.date).all())

    if not start > 1451430000 or end < 1420758000:
        speeches.extend(Speeches2015.query.filter(Speeches2015.pdf.contains(
            keyword)).filter(Speeches2015.date > start).filter(Speeches2015.date < end).order_by(Speeches2015.date).all())

    if not start > 1475186400 or end < 1452466800:
        speeches.extend(Speeches2016.query.filter(Speeches2016.pdf.contains(
            keyword)).filter(Speeches2016.date > start).filter(Speeches2016.date < end).order_by(Speeches2016.date).all())

    if not start > 1514502000 or end < 1483657200:
        speeches.extend(Speeches2017.query.filter(Speeches2017.pdf.contains(
            keyword)).filter(Speeches2017.date > start).filter(Speeches2017.date < end).order_by(Speeches2017.date).all())

    if not start > 1545606000 or end < 1514847600:
        speeches.extend(Speeches2018.query.filter(Speeches2018.pdf.contains(
            keyword)).filter(Speeches2018.date > start).filter(Speeches2018.date < end).order_by(Speeches2018.date).all())

    if not start > 1577401200 or end < 1546815600:
        speeches.extend(Speeches2019.query.filter(Speeches2019.pdf.contains(
            keyword)).filter(Speeches2019.date > start).filter(Speeches2019.date < end).order_by(Speeches2019.date).all())

    if not start > 1609282800 or end < 1578265200:
        speeches.extend(Speeches2020.query.filter(Speeches2020.pdf.contains(
            keyword)).filter(Speeches2020.date > start).filter(Speeches2020.date < end).order_by(Speeches2020.date).all())

    if not start > 1626904800 or end < 1610060400:
        speeches.extend(Speeches2021.query.filter(Speeches2021.pdf.contains(
            keyword)).filter(Speeches2021.date > start).filter(Speeches2021.date < end).order_by(Speeches2021.date).all())

    # If too many speeches are returned, a random sample is taken
    # The size of this sample is defined at the start of the script
    # List size gets reduced to prevent server shutdowns due to (free) hosting limitations

    if len(speeches) > kws_speeches_max:
        speeches = random.sample(speeches, kws_speeches_max)

    speeches.sort(key=lambda speech: speech.date)
    speeches.reverse()

    return speeches

def query_database_area(keyword, area, start, end):
    speeches = []

    if not start > 1293750000 or end < 1263337200:
        speeches.extend(Speeches2010.query.filter(Speeches2010.pdf.contains(
            keyword)).filter(Speeches2010.date > start).filter(Speeches2010.date < end).filter(Speeches2010.country == area).order_by(Speeches2010.date).all())

    if not start > 1325199600 or end < 1294095600:
        speeches.extend(Speeches2011.query.filter(Speeches2011.pdf.contains(
            keyword)).filter(Speeches2011.date > start).filter(Speeches2011.date < end).filter(Speeches2011.country == area).order_by(Speeches2011.date).all())

    if not start > 1355958000 or end < 1325458800:
        speeches.extend(Speeches2012.query.filter(Speeches2012.pdf.contains(
            keyword)).filter(Speeches2012.date > start).filter(Speeches2012.date < end).filter(Speeches2012.country == area).order_by(Speeches2012.date).all())

    if not start > 1388444400 or end < 1357167600:
        speeches.extend(Speeches2013.query.filter(Speeches2013.pdf.contains(
            keyword)).filter(Speeches2013.date > start).filter(Speeches2013.date < end).filter(Speeches2013.country == area).order_by(Speeches2013.date).all())

    if not start > 1418598000 or end < 1388962800:
        speeches.extend(Speeches2014.query.filter(Speeches2014.pdf.contains(
            keyword)).filter(Speeches2014.date > start).filter(Speeches2014.date < end).filter(Speeches2014.country == area).order_by(Speeches2014.date).all())

    if not start > 1451430000 or end < 1420758000:
        speeches.extend(Speeches2015.query.filter(Speeches2015.pdf.contains(
            keyword)).filter(Speeches2015.date > start).filter(Speeches2015.date < end).filter(Speeches2015.country == area).order_by(Speeches2015.date).all())

    if not start > 1475186400 or end < 1452466800:
        speeches.extend(Speeches2016.query.filter(Speeches2016.pdf.contains(
            keyword)).filter(Speeches2016.date > start).filter(Speeches2016.date < end).filter(Speeches2016.country == area).order_by(Speeches2016.date).all())

    if not start > 1514502000 or end < 1483657200:
        speeches.extend(Speeches2017.query.filter(Speeches2017.pdf.contains(
            keyword)).filter(Speeches2017.date > start).filter(Speeches2017.date < end).filter(Speeches2017.country == area).order_by(Speeches2017.date).all())

    if not start > 1545606000 or end < 1514847600:
        speeches.extend(Speeches2018.query.filter(Speeches2018.pdf.contains(
            keyword)).filter(Speeches2018.date > start).filter(Speeches2018.date < end).filter(Speeches2018.country == area).order_by(Speeches2018.date).all())

    if not start > 1577401200 or end < 1546815600:
        speeches.extend(Speeches2019.query.filter(Speeches2019.pdf.contains(
            keyword)).filter(Speeches2019.date > start).filter(Speeches2019.date < end).filter(Speeches2019.country == area).order_by(Speeches2019.date).all())

    if not start > 1609282800 or end < 1578265200:
        speeches.extend(Speeches2020.query.filter(Speeches2020.pdf.contains(
            keyword)).filter(Speeches2020.date > start).filter(Speeches2020.date < end).filter(Speeches2020.country == area).order_by(Speeches2020.date).all())

    if not start > 1626904800 or end < 1610060400:
        speeches.extend(Speeches2021.query.filter(Speeches2021.pdf.contains(
            keyword)).filter(Speeches2021.date > start).filter(Speeches2021.date < end).filter(Speeches2021.country == area).order_by(Speeches2021.date).all())

    # If too many speeches are returned, a random sample is taken
    # The size of this sample is defined at the start of the script
    # List size gets reduced to prevent server shutdowns due to (free) hosting limitations

    if len(speeches) > kws_speeches_max:
        speeches = random.sample(speeches, kws_speeches_max)
        
    speeches.sort(key=lambda speech: speech.date)
    speeches.reverse()
    return speeches

def query_database(keyword=' ', area='all', start=(datetime.utcnow() - timedelta(days=30)).timestamp(), end=datetime.utcnow().timestamp()):

    # Convert the inputs of the dates to date objects

    try:
        start = datetime.fromisoformat(start).timestamp()
    except:
        start = (datetime.utcnow() - timedelta(days=30)).timestamp()

    try:
        end = datetime.fromisoformat(end).timestamp()
    except:
        end = datetime.utcnow().timestamp()   

    # Check for specified area to query, or all get queried

    if area == 'all':
        speeches = query_database_all_area(keyword, area, start, end)
    else:
        speeches = query_database_area(keyword, area, start, end)

    return speeches

# Date filter
@app.template_filter('datefromint')
def format_date(int):
    # Custom filter to format the date object
    # Filter gets applied the jinja2-html template

    date = datetime.fromtimestamp(int)
    date_formatted = date.strftime('%d.%m.%Y')
    return date_formatted


################
# Keyword Search
################

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ################
        # Search Request
        ################

        # Search parameters get collected
        keyword = request.form['keyword']
        area = request.form['area']
        startdate = request.form['startdate']
        enddate = request.form['enddate']

        # Database query and pagination
        speeches = query_database(keyword, area, startdate, enddate)
        speeches_list = pagination(speeches)


        # Plots and Maps creation
        new_wordcloud_path = create_new_wordCloud(speeches)
        new_timeline_path = create_new_timeline(speeches, keyword)
        map_results = create_new_worldmaps(speeches, keyword)
        new_worldmap_path = map_results[0]
        top_countries = map_results[1]

        img_paths = [new_wordcloud_path, new_timeline_path, new_worldmap_path]

        return render_template('index.html', speeches_count=len(speeches), speeches=speeches_list, top_countries=top_countries, img_paths=img_paths)

    if request.method == 'GET':
        #####################
        # Regular Pageload
        #####################

        # Results for default query (all areas, last 30 days)
        speeches = query_database()
        speeches_list = pagination(speeches)

        # Wordcloud can be created without a keyword
        new_wordcloud_path = create_new_wordCloud(speeches)

        # Wordcloud gets shown as placeholders for other plots
        img_paths = [new_wordcloud_path,
                     new_wordcloud_path, new_wordcloud_path]

        return render_template('index.html', speeches_count=len(speeches), speeches=speeches_list, img_paths=img_paths)

    else:
        # This case should never occur. Default query just in case

        speeches = query_database()
        return render_template('tour.html', speeches=speeches)


################
# Topic Modeling
################

def delete_old_tm_results():
    # Search for old scatterplots and delete them
    all_tm_results = glob.glob("static/images/tm_results*")
    for path in all_tm_results:
        os.remove(path)

def topic_modeling(speeches, num_comps):
    if len(speeches) > lda_speeches_max:
        speeches = random.sample(speeches, lda_speeches_max)        
    # Setting up the Vectorizer
    cv = CountVectorizer(max_df=0.8, min_df=0.01, stop_words='english')
    dtm = cv.fit_transform([speech.pdf for speech in speeches])
    LDA = LatentDirichletAllocation(n_components=num_comps)
    LDA.fit(dtm)

    # Get the 15 Top words for each Topic
    topics = []
    for i,topic in enumerate(LDA.components_):
        topics.append([cv.get_feature_names()[index] for index in topic.argsort()[-15:]])
    
    # Prepare the Data for the Plot and overview
    topic_results = LDA.transform(dtm)
    color_names = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    x = []
    y = []
    colors = []
    topic_counter = [0 for topic in enumerate(LDA.components_)]
    
    topic_percentages = [0 for topic in enumerate(LDA.components_)]
    index = 0
    for speech in speeches:
        
        # get the x value
        x.append(datetime.fromtimestamp(speech.date))
        # get the y value
        y.append(topic_results[index][topic_results[index].argmax()])
        # get the color (topic) and add one to the counter list for the topic
        topic_index = topic_results[index].argmax()
        colors.append(color_names[topic_index])
        topic_counter[topic_index] += 1
        index += 1
        

    # Count the counter lists, calculate the percentages and make them into a list. 
    sum = 0
    for index in range(len(topic_counter)):
        sum += topic_counter[index]
    for index in range(len(topic_counter)):
        topic_percentages[index] = round((topic_counter[index] / sum) * 100, 1)

    # Sort the topics by their percentages
    topwords_and_percentages = []
    for index in range(len(topics)):
        percentage = topic_percentages[index]
        word_string = " ".join(list(reversed(topics[index])))
        # topwords_and_percentages.append([topic_percentages[index], list(reversed(topics[index]))])
        topwords_and_percentages.append([percentage, word_string, index])

    # Results in descending order
    topwords_and_percentages.sort()
    topwords_and_percentages.reverse()

    # Create the plot
    delete_old_tm_results()
    plt.clf()
    plt.style.use("dark_background")
    plt.scatter(x, y, c=colors, alpha=0.9)

    # Export as image
    random_path = random_with_N_digits(5)
    new_tm_results_path = "static/images/tm_results" + str(random_path) + ".png"
    plt.savefig(new_tm_results_path, bbox_inches='tight')

    return topwords_and_percentages, new_tm_results_path


@app.route('/topicmodeling', methods=['POST', 'GET'])
def topicmodeling():
    if request.method == 'POST':
        ############
        # TM-Request
        ############

        # Get request parameters
        try:
            number_topics = int(request.form['numbertopics'])
        except:
            number_topics = 3
        area = request.form['area']        
        startdate = request.form['startdate']
        enddate = request.form['enddate']

        # Query database
        speeches = query_database(area=area, start=startdate, end=enddate)

        # Topic Modeling
        results = topic_modeling(speeches, num_comps=number_topics)
        topics = results[0]
        path = results[1]

        return render_template('topicmodeling.html', speeches_count=len(speeches), topics=topics, path=path)

    else:
        # Regular page load
        return render_template('topicmodeling.html')


#############
# Empty Pages
#############
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


#############
# Main script
#############

if __name__ == "__main__":
    
    # Start the app
    app.run()
