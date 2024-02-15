from flask import Blueprint,  jsonify

from blueprints.utils import get_current_user
from models.uploads import file_upload

blueprint = Blueprint("uploads", __name__,url_prefix="/api/uploads")

@blueprint.route("<purchase_order_id>", methods=['POST'])
def upload_handler(purchase_order_id):
    get_current_user()
    return jsonify(file_upload(purchase_order_id))
