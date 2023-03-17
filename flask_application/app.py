import json
import numpy as np
import pandas as pd
import pickle
import requests
import sys
import psycopg2

sys.path.insert(0, '../python_files/')

from flask import Flask, session, request, render_template, redirect, url_for

from data_processing import read_url_content
from data_extraction import extract_keywords
from similarity_matching import find_clusters_for_individual_company

app = Flask(__name__)
app.secret_key = "super_secret_key"
model = pickle.load(open('..\\pickle_files\\finalized_model.sav', 'rb'))
vectorizer = pickle.load(open('..\\pickle_files\\vectorizer.sav', 'rb'))

@app.route('/')
def home():
    #messages = request.args['messages']  # counterpart for url_for()
    if session.get('messages'):
        messages = session['messages']       # counterpart for session
        messages = json.loads(messages)
        session.clear()
        if messages.get('addData'):
            return render_template('index.html', 
                                creation_text = messages['creation_text'],
                                show_addData = messages['show_addData'])
        
        elif messages.get('predict'):
            return render_template('index.html', 
                                prediction_text = messages['prediction_text'],
                                show_predict = messages['show_predict'])
        
    else:
        return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    URL = request.form['url']
    webdata = ""
    try:
        # access the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
        page = requests.get(URL, headers = headers)
        # append the URL content to the list
        webdata = read_url_content(page)
    except(ConnectionError, Exception):
        # for websites not accessible append empty string to the list
        webdata = ""
    
    keywords = extract_keywords(webdata)

    test_company_input = vectorizer.transform([keywords]).toarray().tolist()
    prediction = model.predict(test_company_input)

    print(prediction[0])

    if(prediction == 1):
        main_cluster, sub_cluster = find_clusters_for_individual_company(keywords)
        prediction_text= 'It is an AI company for Product Creation with Main Cluster - {} & Sub Cluster - {}'.format(main_cluster, sub_cluster)
    else:
        prediction_text='It is not an AI company for Product Creation'
    
    messages = json.dumps({
        "predict": True,
        "prediction_text": prediction_text,
        "show_predict": "style=display:block;"
    })

    session['messages'] = messages
    
    return redirect(url_for('home', messages = messages))


def get_db_connection():#TODO: Remove hardcoded connection strings
    conn = psycopg2.connect(host="127.0.0.1",
                            database='postgres',
                            user="postgres",
                            port= 5432,
                            password='Chaitali@28')
    return conn

@app.route('/addData', methods=['GET', 'POST'])
def addData():
    name = request.form['name']
    product = request.form['product']
    cluster = request.form['cluster']
    sub_cluster = request.form['sub-cluster']
    link = request.form['company_url']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO PRODCREATION_COMPANIES(COMPANY_NAME,PRODUCT,COMPANY_CLUSTER,COMPANY_SUBCLUSTER,COMPANY_LINK)"
                "VALUES(%s, %s, %s, %s, %s)",
                (name, product, cluster, sub_cluster, link))
    conn.commit()
    cur.close()
    conn.close()

    print("Company {} added successfully".format(name))

    messages = json.dumps({
        "addData": True,
        "creation_text": "Successfully added the Company {} with Product {} to Database".format(name, product),
        "show_addData": "style=display:block;"
        })
    
    session['messages'] = messages
    
    return redirect(url_for('home', messages = messages)) 
    #render_template('index.html', creation_text = "Successfully added the Company {} with Product {} to Database".format(name, product), show_addData="style=visibility:visible;")

if __name__ == "__main__":
    app.run(debug=True, port=7000)