from flask import Flask, redirect, url_for
from flask_admin import Admin

from App.Common.config import PANEL_SECRET
from App.Common.storage import session_builder
from App.Model.Backend import Backend, BackendView

app = Flask(__name__)
app.secret_key = PANEL_SECRET

admin = Admin(app)
admin.add_view(BackendView(Backend, session_builder()))


@app.route("/")
def index():
    return redirect(url_for("admin.index"))
