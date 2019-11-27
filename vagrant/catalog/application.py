#! /usr/bin/env python

import requests
from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash, session as login_session, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_setup import Category, CategoryItems, Users, Base
import random
import string
import httplib2
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

# get the google security information from the local file
CLIENT_ID = json.loads(
    open('client_secret_192267253440-2etbqvgktmhbpd3il2t10oed4f73ocks.apps.googleusercontent.com.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Web Application 1"

# Connect to the Database and create a database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Login w/ token
@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
# def gconnect2():
#     if request.args.get('state') != login_session['state']:
#         response = make_response(json.dumps('Invalid state parameter.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
    
#     ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
#     AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'   
#     CLIENT_ID = json.loads(open('google_key.json','r').read())['web']['client_id']
#     CLIENT_SECRET = json.loads(open('google_key.json','r').read())['web']['client_secret']

#     try:


def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('google_key.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

#Disconnect Session

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#show categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category)
    return render_template('categories.html', categories = categories)

#New Categories
@app.route('/category/new', methods=['GET','POST'])
def newCategory():

    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)

        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_tempalate('newCategory.html')

#Delete Categories
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    catToDelete = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        session.delete(catToDelete)
        session.commit()
        return redirect(url_for('showCategories', category_id = category_id))
    else:
        return render_template('deleteCategory.html', category=catToDelete)

#Edit Categories
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    catToEdit = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        if request.form['name']:
            catToEdit.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=catToEdit)

#Show Items
@app.route('/category/<int:category_id>/item/')
def showItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('items.html', items=items,category=category)

#New Items
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):

    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'],
                        category_id = category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItem', category_id = category_id))
    else:
        return render_template('newCategoryItem.html', category_id = category_id)

#Edit Item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):

    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        
        session.add(editedItem)
        session.commit()

        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('editedItem.html', category_id=category_id, item_id=item_id, item=editedItem)

#Delete Item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):

    delItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        session.delete(delItem)
        session.commit()

        return redirect(url_for('showItem', category_id = category_id))
    else:
        return render_template('delItem.html', item=delItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)