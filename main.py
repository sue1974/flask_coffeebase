from flask import Flask, render_template, redirect, url_for

import config
from models import db, Coffee
from mongoengine.queryset.visitor import Q


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['HOST'] = '0.0.0.0'
    flask_app.config['DEBUG'] = True
    flask_app.config['PORT'] = 9000

    # connection to MongoDB
    flask_app.config['MONGODB_SETTINGS'] = {
        'db': config.MONGO_DB,
        'host': config.MONGO_HOST,
        'port': config.MONGO_PORT,
        'username': config.MONGO_USERNAME,
        'password': config.MONGO_PASSWORD,
        'authentication_source': config.MONGO_AUTHENTIFICATION_SOURCE
    }

    db.init_app(flask_app)

    return flask_app


app = create_app()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index/<cof_user_id>')
def index(cof_user_id):
    # coffees = Coffee.objects.delete()
    coffees = Coffee.objects(cof_user_id=cof_user_id).order_by('-cof_date').limit(50)
    counter_false = Coffee.objects(Q(cof_user_id=cof_user_id) & Q(cof_payed=False)).count()
    counter_all = Coffee.objects(cof_user_id=cof_user_id).count()
    return render_template('index.html', coffees=coffees, counter_false=counter_false, counter_all=counter_all,
                           user=cof_user_id)


@app.route('/add_coffee/<cof_user_id>')
def add_coffee(cof_user_id):
    # Create new Coffee
    coffee = Coffee(cof_user_id=cof_user_id)

    try:
        coffee.save()
        return redirect(url_for('index', cof_user_id=cof_user_id))
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/pay_coffee/<cof_user_id>')
def pay_coffee(cof_user_id):
    coffees = Coffee.objects(cof_user_id=cof_user_id)

    for coffee in coffees:
        coffee.cof_payed = True
        coffee.save()

    return redirect(url_for('index', cof_user_id=cof_user_id))


if __name__ == '__main__':
    print('Direkter Start über Console mit [python3 main.py]')
    port = app.config.get('PORT')
    app.run(host=app.config.get('HOST'), debug=app.config.get('DEBUG'), port=app.config.get('PORT'))
