# coding: utf-8

from contextlib import contextmanager

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


db = SQLAlchemy(session_options={
    'expire_on_commit': False,
    'autoflush': False,
})


class Base(db.Model):
    __abstract__ = True


def _unique_suffix(target, primary_key):
    return '-'.join(map(lambda k: str(getattr(target, k.name)), primary_key))


def _unique_key(target, primary_key):
    key = _unique_suffix(target, primary_key)
    return target.generate_cache_prefix('get') + key


def _itervalues(data, idents):
    for k in idents:
        item = data[str(k)]
        if item is not None:
            yield item
