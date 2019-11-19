from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_admin.contrib.sqla import ModelView
from App.Common.config import DB_URI

engine = create_engine(DB_URI)
base = declarative_base(bind=engine)


def session_builder():
    return scoped_session(sessionmaker(bind=engine))


class AppModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model=model, session=session, name=name, category=category, endpoint=endpoint, url=url,
                         static_folder=static_folder, menu_class_name=menu_class_name, menu_icon_type=menu_icon_type,
                         menu_icon_value=menu_icon_value, )
