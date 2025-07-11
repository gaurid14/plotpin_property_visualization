from flask import Flask, url_for, redirect, request
from flask import render_template
from flask import Blueprint
from flaskr.map.map import create_dash_app
# bp = Blueprint('app', __name__)

def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.secret_key=b'_5#y2L"F4Q8z\n\xec]/'
    create_dash_app(app)
    #Register blueprints from subdirectories
    # from flaskr.map.near_station_property import bp as near_station_bp
    from flaskr.map.recommended_property import bp as recommended_bp
    from flaskr.map.map import bp as map_bp
    from flaskr.map.filtered_property import bp as filtered_property_bp
    from flaskr.user_data.login import bp as login_bp
    from flaskr.user_data.registration import bp as registration_bp
    from flaskr.user_data.session import bp as session_bp
    # from flaskr.map.search_within_area import bp as search_within_bp
    from flaskr.map.trending_property import bp as trending_bp
    from flaskr.map.geocoding import bp as geocoding_bp
    # from flaskr.map.recommend_property import bp as recommend_property_bp

    # app.register_blueprint(near_station_bp)
    app.register_blueprint(recommended_bp)
    app.register_blueprint(filtered_property_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(map_bp, url_prefix='/map')
    app.register_blueprint(registration_bp)
    # app.register_blueprint(search_within_bp)
    app.register_blueprint(trending_bp)
    app.register_blueprint(geocoding_bp)
    # app.register_blueprint(recommend_property_bp)

    # @app.route('/')
    # def default():
    #     return redirect(url_for('login'))

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/registration')
    def registration():
        # print("Rendering registration.html")  # Add debug output
        return render_template('registration.html')

    @app.route('/home')
    def home():
        # print("Rendering registration.html")  # Add debug output
        return render_template('home.html')

    @app.route('/explore')
    def explore():
        new_content = "<h2>New content for exploration</h2>"
        return render_template('explore.html')
        # return render_template('explore.html', content=create_dash_app(app))

    @app.route('/mumbai')
    def mumbai():
        location = request.args.get('location')
        return render_template('mumbai.html', location=location)

    @app.route('/bangalore')
    def bangalore():
        location = request.args.get('location')
        return render_template('bangalore.html', location=location)

    @app.route('/new_delhi')
    def new_delhi():
        location = request.args.get('location')
        return render_template('new_delhi.html', location=location)
    # @app.errorhandler(404)
    # def not_found(error):
    #     return render_template('error.html'), 404
    # @app.route('/explore')
    # def explore():
    #     new_content = "<h2>New content for exploration</h2>"
    #     return render_template('trending_property.py', content=new_content)

    return app


if __name__ == '__main__':
    app = create_app()
    # create_dash_app(app)
    app.run(host = '192.168.0.147', port = 5000, debug = True)
