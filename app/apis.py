import json

from app import app
from app.db.comments import Comment
from app.db.galleries import Gallery
from app.db.subscriptions import Subscription
from app.utils.aws import s3_change_image_resolutions
from app.utils.email import send_contact_email

from flask import request


@app.route('/send/email', methods=['POST'])
def email_message():
    data = json.loads(request.data)
    email = data.get('email')
    subject = data.get('subject')
    body = data.get('body')
    if not email or not body:
        return_data = {'message': 'An email and body are required.'}
        return json.dumps(return_data), 500, {'Content-Type': 'application/json'}
    send_contact_email(email, subject, body)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@app.route('/blog/<uuid>/comments', methods=['GET'])
def blog_comments(uuid):
    tweets = Comment.get_comments_json(gallery_uuid=uuid, sort_by='-created_at')
    data = {'comments': tweets, 'num_comments': len(tweets)}
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@app.route('/images/generate_sizes', methods=['POST'])
def create_multiple_photos():
    data = json.loads(request.data)
    s3_change_image_resolutions(data['image_route'], data['filename'])
    data = {'message': 'success'}
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@app.route('/subscriptions/subscribe', methods=['POST'])
def subscribe():
    data = json.loads(request.data)
    subscription, message = Subscription.create_or_update(**data)
    message = {"message": message}
    return json.dumps(message), 200, {'Content-Type': 'application/json'}


@app.route('/gallery/<uuid>', methods=['GET'])
def get_gallery_ajax(uuid):
    gallery = Gallery.get(uuid=uuid)
    return json.dumps(gallery.to_dict()), 200, {'Content-Type': 'application/json'}


@app.route('/ping', methods=["GET"])
def ping():
    return '', 200
