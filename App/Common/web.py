from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import BaseModelView
from App.Common.storage import session
from App.Model.Backend import Backend, backend_desc, backend_label
from App.Common.config import PANEL_SECRET

app = Flask(__name__)
app.secret_key = PANEL_SECRET

admin = Admin(app)

class BackendModelView

base_model = ModelView(Backend, session())
base_model.column_labels = backend_label
base_model.column_descriptions = backend_desc
admin.add_view(base_model)


@app.route("/")
def index():
    return redirect(url_for("admin.index"))
