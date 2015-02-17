# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2015 John Dewey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from contextlib import contextmanager
from sqlalchemy import orm

from pbr import version

from demeter import client

engine = client.get_engine()
session_factory = orm.sessionmaker(bind=engine)
Session = orm.scoped_session(session_factory)

try:
    version_info = version.VersionInfo('demeter')
    __version__ = version_info.version_string()
except AttributeError:
    __version__ = None


@contextmanager
def transactional_session():
    """
    Provide a transactional scope around a series of operations.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    # TODO(retr0h): Figure out how to handle sessions better.
    # finally:
    #     session.close()


@contextmanager
def temp_session():
    """
    Simple context manager that provides a temporary Session object to the
    nested block.
    """
    session = Session()
    try:
        yield session
    except:
        raise
    # TODO(retr0h): Figure out how to handle sessions better.
    # finally:
    #     session.close()
