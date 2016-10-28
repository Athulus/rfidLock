# This is mostly a CRUD package for accessing the database of users
# There are certain

import hashlib
from base64 import b64encode
from contextlib import closing
from datetime import datetime

# Used to abstract database details a little bit more
class MemberDatabase(object):
  """
  An object used to abstract details of the member database from direct access.

  Internally, email addresses and hashes must be unique when added to the 
  database.

  The RFID data is hashed before use to prevent abuse
  """
  def __init__(self, db, subs):
    """
    db - database object to use
    subs - substitution expression for the database in use
    """
    self.db = db
    # Technically, emails may be 254 characters at most
    self.start_query = u"""
      CREATE TABLE member_table (
        hash CHAR(24),
        name TEXT,
        email VARCHAR(254),
        expiration_date DATE,
        CONSTRAINT pk_hash PRIMARY KEY(hash),
        CONSTRAINT unique_email UNIQUE(email));
      """
    self.destroy_query = u"""
      DROP TABLE member_table;
      """
    self.add_query = u"""
      INSERT INTO member_table (name, email, hash, expiration_date) VALUES ({0}, {0}, {0}, {0});
      """.format(subs)
    self.have_query = u"""
      SELECT COUNT(hash) FROM member_table WHERE hash={0};
      """.format(subs)
    self.have_current_query = u"""
      SELECT COUNT(hash) FROM member_table WHERE hash={0} AND expiration_date > {0};
      """.format(subs)
    self.list_query = u"""
      SELECT name, email, expiration_date FROM member_table;
      """
    self.content_query = u"""
      SELECT hash, name, email, expiration_date FROM member_table;
      """
    self.clone_query = u"""
      INSERT INTO member_table (hash, name, email, expiration_date) VALUES ({0}, {0}, {0}, {0});
      """.format(subs)
    self.record_query = u"""
      SELECT hash, name, email, expiration_date FROM member_table WHERE hash={0};
      """.format(subs)
  @staticmethod
  def hash(card_data):
    """Hashes the provided RFID data using MD5"""
    m = hashlib.md5()
    m.update(card_data)
    # Needs to go through this for Python2 support
    # Binary data is hard to work with across versions
    return b64encode(m.digest()).decode()
  def add(self, card_data, member_name, member_email, expiration):
    """Adds a new member to the list of members"""
    with closing(self.db.cursor()) as cur:
      cur.execute(self.add_query, (member_name, member_email, MemberDatabase.hash(card_data), expiration))
    self.db.commit()
  def have(self, card_data):
    """
    Uses the hash of the member's RFID data to check whether they have ever
    been a member.
    """
    with closing(self.db.cursor()) as cur:
      cur.execute(self.have_query, (MemberDatabase.hash(card_data), ))
      return cur.fetchone()[0] > 0
  def have_current(self, card_data):
    """
    Uses the member's RFID data to check whether they are a current member.
    """
    with closing(self.db.cursor()) as cur:
      cur.execute(self.have_current_query, (MemberDatabase.hash(card_data), datetime.now()))
      return cur.fetchone()[0] > 0
  def list(self):
    """Retrieves a list of all members and former members"""
    with closing(self.db.cursor()) as cur:
      cur.execute(self.list_query)
      return cur.fetchall()
  def create(self):
    """Creates the tables necessary for the membership system"""
    with closing(self.db.cursor()) as cur:
      cur.execute(self.start_query)
    self.db.commit()
  def destroy(self):
    """Removes the tables created for this system"""
    with closing(self.db.cursor()) as cur:
      cur.execute(self.destroy_query)
    self.db.commit()
  def clear(self):
    """Resets the contents of this database to be empty"""
    self.destroy()
    self.create()
  def mimic(self, other):
    """Makes this database identical to the provided database"""
    self.clear()
    with closing(self.db.cursor()) as cur, closing(other.db.cursor()) as othercur:
      othercur.execute(other.content_query)
      for entry in othercur:
        cur.execute(self.clone_query, entry)
    self.db.commit()
  def sync(self, other, card_data):
    """Updates a singular record from a different database"""
    with closing(self.db.cursor()) as cur, closing(other.db.cursor()) as othercur:
      othercur.execute(other.record_query, (MemberDatabase.hash(card_data), ))
      cur.execute(self.clone_query, othercur.fetchone())
    self.db.commit()
