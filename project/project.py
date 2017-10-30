from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Tool, Link

# app name
app = Flask(__name__)

# sqlalchemy to access db
engine = create_engine('sqlite:///researchtool.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# common info 
meta_title = ' Design Research'
meta_desc = 'Design research resources and links to keep interests in projects.'
meta_url = 'URL_MAIN'


# flask's decoration
# '/' will run hello function
@app.route('/')
def main():
    # render tempaltes, using Flask function
    categories = session.query(Category).all()
    return render_template('main.html', meta_title=meta_title, meta_desc=meta_desc, categories=categories)


# category
@app.route('/<string:category_name>')
def category(category_name):
    categories = session.query(Category).all()
    category_name = category_name.title()
    category = session.query(Category).filter_by(name=category_name).one()
    cat_id = category.id
    tools = session.query(Tool).filter_by(cat_id=cat_id).all()

    tool_id_list =[]
    for i in tools:
        tool_id_list.append(i.id)
    
    links = None;
    for i in tool_id_list:
        q1 = session.query(Link).filter_by(tool_id=i).all()
        if links is None:
            links = q1
        else:
            links = links.append(q1)

    return render_template('category.html', meta_title=meta_title, meta_desc=meta_desc,
                           categories=categories, category=category, tools=tools, links=links)

# return link list
def get_link(tool_id):
    links = session.query(Link).filter_by(toold_id=tool_id).all()
    return links

# new
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else: 
        return render_template('new.html', restaurant_id=restaurant_id)


# edit
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("new menu item has created.")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# delete
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("The menu item has deleted.")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete.html', item=deleteItem)


# return JSON
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    # let hear any webserver
    app.run(host='0.0.0.0', port = 5000)
