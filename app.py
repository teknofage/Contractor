# # db.penguin_items.insertOne({"" : "", "" : "", "" : "", "" : ""})
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/One Stop Penguin Shop')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
penguin_items = db.penguin_items
comments = db.comments

app = Flask(__name__)


@app.route('/')
def penguin_items_index():
    """Show all penguin related items."""
    return render_template('penguin_items_index.html', penguin_items=penguin_items.find())


@app.route('/carts', methods=['POST'])
def playlists_submit():
    """Submit a new shopping cart."""
    cart = {
        'Item Name': request.form.get('Item Name'),
        'Image': request.form.get('Image'),
        'Description': request.form.get('Description'),
        'Item Type': request.form.get('Item Type'),
        'Ratings': request.form.get('Ratings')
    }
    cart_id = carts.insert_one(cart).inserted_id
    return redirect(url_for('carts_show', cart_id=cart_id))


@app.route('/cart/new')
def cart_new():
    """Create a new shopping cart."""
    return render_template('cart_new.html', cart={}, title='New Cart')


@app.route('/carts/<cart_id>')
def carts_show(cart_id):
    """Show your shopping cart."""
    cart = carts.find_one({'_id': ObjectId(cart_id)})
    return render_template('carts_show.html', cart=cart)

@app.route('/items/<item_id>')
def item_show(item_id):
    """Show item information."""
    item = items.find_one({'_id': ObjectId(item_id)})
    item_comments = comments.find({'item_id': ObjectId(item_id)})
    return render_template('items_show.html', item=item, comments=items_comments)

@app.route('/categories/<category_id>')
def category_show(category_id):
    """Show categories."""
    category = category.find_one({'_id': ObjectId(category_id)})
    return render_template('category_show.html', category=category)


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))


@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))