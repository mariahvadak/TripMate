from app import create_app

app = create_app()

if __name__ == '__main__':
    app.config['STATIC_PATH'] = 'app/static/'
    app.run(host="localhost", port=8000, debug=True)