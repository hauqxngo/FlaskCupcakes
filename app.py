"""Flask app for Cupcakes"""

from flask import Flask, json, render_template, jsonify, request

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

#############################################################################

@app.route('/')
def index():
    """Show homepage."""

    return render_template('index.html')


@app.route('/api/cupcakes')
def list_cupcakes():
    """List all cupcakes.
    
    Returns JSON like: {cupcakes: [{id, flavor, rating, size, image}, ...]}"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcake=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake.

    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake.

    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}."""

    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    res_json = jsonify(cupcake=new_cupcake.serialize())
    return (res_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update the current id cupcake."""

    cupcake = Cupcake.query.get_or_404(id)

    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete the current id cupcake."""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='deleted')


