from flask import Blueprint, request
from apifairy import body, response, other_responses
from .schema import NotificationSchema
from .broker_routes import publishGetNots, publishGetNot, publishPostNot, publishDeleteNot

bp = Blueprint('notification', __name__, url_prefix='/notifications')

notification_schema = NotificationSchema()
@bp.route('/<int:notification_id>', methods=['GET'])
@response(notification_schema, 200)
def get_notification(notification_id):
    """Retrieve a notification by id"""
    return publishGetNot(notification_id) 


@bp.route('/', methods=['GET'])
@response(notification_schema, 200)
def get_notifications():
    """Retrieve notifications list"""
    return publishGetNots()


@bp.route('/', methods=['POST'])
@response(notification_schema, 201)
@body(notification_schema, 201)
def post_notification():
    """Create a notification"""
    payload = request.get_json()
    return publishPostNot(payload)


@bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a notification by id"""
    return publishDeleteNot(notification_id)
