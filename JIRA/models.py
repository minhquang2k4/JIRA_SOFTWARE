from dataclasses import dataclass
from datetime import datetime

from JIRA import db, bcrypt, login_manager, scheduler, app

class User(db.Model, UserMixin):
  """
  UserMixin là một class có sẵn trong flask_login để hỗ trợ việc quản lý user
  """
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  username = db.Column(db.String(100), nullable=False)
  password_hashed = db.Column(db.String(100), nullable=False)
  active = db.Column(db.Boolean, default=True)
  phone = db.Column(db.String(100))
  email = db.Column(db.String(100))
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  create_uid = db.Column(db.Integer, default=0)
  write_uid = db.Column(db.Integer, default=0)
  is_admin = db.Column(db.Boolean, default=False)
  db.UniqueConstraint(username, email)

  @property  # Decorator này dùng để tạo ra một thuộc tính giả
  def password(self):
    if self.password_hashed is not None:
      return None
    return self.password

  @password.setter
  def password(self, password):
    """
    Hàm này được sử dụng để mã hóa password
    :param password:
    :return:
    """
    self.password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    """
    Hàm này được sử dụng để kiểm tra password đã được mã hóa có khớp với password người dùng nhập vào hay không
    :param attempted_password:
    :return:
    """
    return bcrypt.check_password_hash(self.password_hashed, attempted_password)

  def __repr__(self):
    return '<User %r>' % self.username
