from app import create_app
app = create_app()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],host='0.0.0.0',port=82,threaded=True)