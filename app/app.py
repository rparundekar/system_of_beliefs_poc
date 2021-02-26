## This is the flask endpoint for remembering and retrieving Beliefs.
import traceback
from flask import Flask, request, redirect
from flask_cors import CORS
import belief_helper

# The flask api for serving endpoints
app = Flask(__name__, static_url_path='', 
            static_folder='/app/static')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return redirect("/index.html")

@app.route('/health_check', methods=['GET'])
def ping():
    """ Healthcheck """
    return "ok", 200

@app.route('/beliefs', methods=['POST'])
def remember_belief():
    belief_text = request.get_data()
    err, belief_obj = belief_helper.validate(belief_text)
    belief_helper.remember_belief(belief_text)
    if err: return err, 422
    return belief, 200

@app.route('/beliefs/<belief_id>', methods=['GET'])
def get_belief(belief_id):
    err, presigned_url = belief_helper.get_belief(belief_id)
    if err: return err, 422
    return redirect(presigned_url)


