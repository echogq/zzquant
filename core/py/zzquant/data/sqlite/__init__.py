# coding: utf-8

import json
from contextlib import contextmanager
from sqlalchemy import inspect, types, TypeDecorator


def make_url(location, filename):
    db_file = location+filename
    return 'sqlite:///{}'.format(db_file)


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@contextmanager
def session_scope(session_factory):
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Json(TypeDecorator):
    @property
    def python_type(self):
        return object

    impl = types.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None

class EnumTypeDecorator(TypeDecorator):
    impl = types.Integer
    def __init__(self, enum_type):
        TypeDecorator.__init__(self)
        self.enum_type = enum_type

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        return int(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return self.enum_type(value)
        except (ValueError, TypeError):
            return None

class UINT64(TypeDecorator):
    impl = types.String

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None