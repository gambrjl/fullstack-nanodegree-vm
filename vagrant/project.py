#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, flash, session as login_session
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import random, string

#Create and Connect to database
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return "The Current State is %s" % login_session['state']

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    """ output = "<h1>%s</h1>" % restaurant.name
    for item in items:
        output += "<p>"
        output += item.name
        output += "<br />"
        output += item.price
        output += "<br />"
        output += item.description
        output += "<br />" """
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/newItem/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/editItem/')
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:    
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deleteItem/')
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', item = deletedItem )

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)