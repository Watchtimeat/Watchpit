from flask import Flask, jsonify
from flask_cors import CORS

from blueprints import auth, functions, products, purchase_invoices, purchase_orders, resources, users,uploads,service_orders,estoklus,customers,html,pdf,wpp,mail

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "supports_credentials": True
}})
app.register_blueprint(auth.blueprint)
app.register_blueprint(functions.blueprint)
app.register_blueprint(products.blueprint)
app.register_blueprint(purchase_invoices.blueprint)
app.register_blueprint(purchase_orders.blueprint)
app.register_blueprint(resources.blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(uploads.blueprint)
app.register_blueprint(service_orders.blueprint)
app.register_blueprint(estoklus.blueprint)
app.register_blueprint(customers.blueprint)
app.register_blueprint(html.blueprint)
app.register_blueprint(pdf.blueprint)
app.register_blueprint(wpp.blueprint)
app.register_blueprint(mail.blueprint)


@app.errorhandler(400)
def badrequest(error):
    response = jsonify(message=error.description)
    response.status_code = 400
    return response


@app.errorhandler(401)
def unauthorized(error):
    print(error.description)
    response = jsonify(message=error.description)
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(error):
    response = jsonify(message=error.description)
    response.status_code = 403
    return response
