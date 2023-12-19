from main import app
import config

if __name__ == "__main__":
    print("Start von wsgi.py auf NGINX - Server")
    app.run(debug=config.DEBUG)
