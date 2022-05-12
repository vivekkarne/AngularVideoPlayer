from ctypes import sizeof
from email import header
from fileinput import filename
from os import O_TRUNC
import os
from urllib import response
from flask import Flask, abort, jsonify, make_response, render_template, request, redirect, url_for, Response
from flask_pymongo import PyMongo, ObjectId
from gridfs import GridFSBucket, GridFS
from flask_cors import CORS, cross_origin
from gridfs.errors import NoFile
import mimetypes
import cv2
import numpy as np


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pymongo"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
mongo = PyMongo(app)
grid = GridFS(mongo.db)
gridBucket = GridFSBucket(mongo.db)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
@cross_origin()
def upload_file():
    print(request.files['video'])
    video_file = request.files['video']
    oid = grid.put(video_file, content_type = video_file.content_type, filename=video_file.filename)
    response = jsonify({"id": str(oid)})
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type');
    response.status_code = 200
    return response

@app.route('/files/<oid>', methods=["GET"])
@cross_origin()
def serve_gridfs_file(oid):
    try:
        file = mongo.db.fs.files.find_one({"_id": ObjectId(oid)})
        
        # chunks = mongo.db.fs.chunks.find({'files_id': file['_id']}).sort('n')
        grid_out = gridBucket.open_download_stream(file['_id'])
        bleh = grid_out.read()
        # print(type(bleh))

        # #bytes to array
        # vid = np.frombuffer(bleh, dtype=np.uint8)
        # gray = cv2.cvtColor(vid, cv2.COLOR_BAYER_BG2GRAY)

        # while True:

        #     ret, img = grid_out.read()

        #     gray = cv2.cvtColor(vid, cv2.COLOR_BAYER_BG2GRAY)


        response = Response(bleh)
        print(type(bleh))
        print(len(bleh))
        response.headers['Content-Length'] = file['length']

        if 'contentType' in file:
            response.headers['Content-Type'] = file['contentType']
        else:
            response.headers['Content-Type'] = mimetypes.guess_type(file.filename)[0]
        return response
    except NoFile:
        abort(404)

@app.route('/gscale/<oid>', methods=["GET"])
@cross_origin()
def show_grayscale(oid):
    try:
        file = mongo.db.fs.files.find_one({"_id": ObjectId(oid)})
        
        # chunks = mongo.db.fs.chunks.find({'files_id': file['_id']}).sort('n')
        file_o = open('mov.mp4', 'wb+')
        gridBucket.download_to_stream(file['_id'], file_o)

        file_o.seek(0)
        
        source = cv2.VideoCapture('mov.mp4')

        (m_v, min_v, subm_v) = (cv2.__version__).split('.')

        if int(m_v) < 3:
            fps = source.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = source.get(cv2.CAP_PROP_FPS)
        
        print(fps)
        # We need to set resolutions. 
        # so, convert them from float to integer. 
        frame_width = int(source.get(3)) 
        frame_height = int(source.get(4)) 
        

        size = (frame_width, frame_height)
        result = cv2.VideoWriter('static/converted/gray.webm',  
            cv2.VideoWriter_fourcc(*'vp80'), 
            fps, size, 0)
        
        # running the loop 
        while True: 
        
            # extracting the frames 
            ret, img = source.read() 
            
            # converting to gray-scale 
            if ret:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            else:
                break
            # write to gray-scale 
            result.write(gray)


            # exiting the loop 
            key = cv2.waitKey(1) 
            if key == ord("q"): 
                break
            
        source.release()

        return redirect(url_for('static', filename='converted/gray.webm'))
    except NoFile:
        abort(404)