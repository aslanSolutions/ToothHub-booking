from flask import Blueprint
from apifairy import body, response, other_responses
from .schema import NotificationSchema

bp = Blueprint('notification', __name__, url_prefix='/notifications')

notification_schema = NotificationSchema()

@bp.route('/<int:notification_id>', methods=['GET'])
@other_responses({404: 'Notification details not found'})
@response(notification_schema, 200)
def get_delivery(notification_id):
    """retrieve a Notification by id"""
    return "Hello World"