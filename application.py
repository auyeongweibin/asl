from flask import Flask, render_template, Response
import ultralytics
from resources.detect import detect

def create_app(config_filename):
    application = app = Flask(__name__, static_url_path='')
    application.config.from_object(config_filename)

    PATH = 'model/best.pt'
    model = ultralytics.YOLO(PATH)

    return [application, model]

app, model = create_app("config")
application = app

@application.route('/', methods=['GET'])

def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return Response(detect(model), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    application.run()