from app import app

if __name__ == "__main__":
    app.run()


# gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
#sudo apt-get install libmariadb-dev
