from database.db import db
from database.models import Post, Image
from flask_restful import Resource
from config import FORMAT_STRING_DATETIME
from flask import Response, jsonify


class PostsApi(Resource):
    def get(self):
        posts = db.session.query(Post).limit(1).all()
        for i in range(len(posts)):
            posts[i] = posts[i].as_dict()
            posts[i]['time_upload'] = posts[i]['time_upload'].strftime(FORMAT_STRING_DATETIME)
            posts[i]['time_priority'] = posts[i]['time_priority'].strftime(FORMAT_STRING_DATETIME)

            images = db.session.query(Image).filter(Image.post_id == posts[i]['post_id']).all()
            posts[i]['images'] = [str(image) for image in images]
        return jsonify(posts)
        # return Response(posts, mimetype="application/json", status=200)
