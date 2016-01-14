from flask import Flask, request, render_template
import json
import socket
import cfmodel
from getfeatures import Featurize
from predict import Predict
from bias import BiasScoring
import pickle, re, requests
from bs4 import BeautifulSoup
from flask.ext.paginate import Pagination

app = Flask(__name__)
PORT = 5353


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():

    search = request.form['text']
    processed_search = search.replace(' ', '+')
    googlenews = "https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q="+processed_search
    
    user_agent = {'User-agent': 'Mozilla/5.0 ;Macintosh; Intel Mac OS X 10_10_2; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.111 Safari/537.36'}
    sesh = requests.Session()
    r = sesh.get(googlenews, headers=user_agent)
    soup = BeautifulSoup(r.content, 'html.parser')
    items = soup.find("a", {'class':'_T6c'})
    key = re.search('ncl=(.*)&amp;q', str(items))
    key = key.group(1)

    url = "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&q="+processed_search+"&cf=all&ncl="+key+"&output=rss&num=500"

    return search_results(url)

@app.route('/search')
def search_results(url):

    score = BiasScoring(url)
    score.parallelize_articlize()
    predict = Predict()

    # pred, articles = predict.featurize_predict(score.articles)

    # i=0

    # for k, v in score.article_rank.items():
    #     score.article_rank[k]['prediction'] = pred[i]
    #     print score.article_rank[k]['prediction']
    #     i+=1


    page = int(request.args.get('page', 1))


    pagination = Pagination(page=page, total=len(score.article_rank), search=False, record_name='score.article_rank', css_framework='foundation')
    return render_template('search.html', data=score.article_info, pagination=pagination)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=PORT, debug=True)