from flask import Blueprint
from apifairy import body, response, other_responses
from .schema import NotificationSchema

bp = Blueprint('notification', __name__, url_prefix='/notifications')

notification_schema = NotificationSchema()

@bp.route('/<int:notification_id>', methods=['GET'])
@other_responses({404: 'Notification not found'})
@response(notification_schema, 200)
def get_notification(notification_id):
    """Retrieve a notification by id"""
    return "Hello World"

@bp.route('/', methods=['GET'])
@other_responses({404: 'Notification not found'})
@response(notification_schema, 200)
def get_notifications(notification_id):
    """Retrieve all notifications list"""
    return "Hello World"


@bp.route('/', methods=['POST'])
@other_responses({501: 'Notification could not be sent'})
@response(notification_schema, 201)
def post_notification(notification_id):
    """Create a notification"""
    return "Hello World"

@bp.route('/<int:notification_id>', methods=['DELETE'])
@other_responses({404: 'Notification not found'})
def delete_notification(notification_id):
    """Delete a notification by id"""
    return "Hello World"