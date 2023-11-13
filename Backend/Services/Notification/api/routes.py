from flask import Blueprint
from apifairy import body, response, other_responses
from .schema import NotificationSchema
from .broker_routes import publishGetNots, publishGetNot, publishPostNot, publishDeleteNot

bp = Blueprint('notification', __name__, url_prefix='/notifications')

notification_schema = NotificationSchema()
@bp.route('/<int:notification_id>', methods=['GET'])
@other_responses({404: 'Notification not found'})
@response(notification_schema, 200)
def get_notification(notification_id):
    """Retrieve a notification by id"""
    publishGetNot(notification_id)


@bp.route('/', methods=['GET'])
@other_responses({404: 'No notifications found'})
@response(notification_schema, 200)
def get_notifications():
    """Retrieve notifications list"""
    publishGetNots()


@bp.route('/', methods=['POST'])
@other_responses({501: 'Notification could not be sent'})
@response(notification_schema, 201)
@body(notification_schema, 201)
def post_notification(notification_id):
    """Create a notification"""
    publishPostNot(notification_id)


@bp.route('/<int:notification_id>', methods=['DELETE'])
@other_responses({404: 'Notification not found'})
def delete_notification(notification_id):
    """Delete a notification by id"""
    publishDeleteNot(notification_id)
