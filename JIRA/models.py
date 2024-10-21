from dataclasses import dataclass
from datetime import datetime
from flask_login import UserMixin

from JIRA import db, bcrypt, login_manager



@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


# khi 1 lớp kế thừa db.Model thì nó sẽ tạo ra 1 bảng trong database tên mặc định sẽ là tên của lớp đó viết thường
# nếu muốn đặt tên khác thì dùng __tablename__ = 'tên bảng'
class User(db.Model, UserMixin):
  # UserMixin là một class có sẵn trong flask_login để hỗ trợ, cung cấp những phương thức cần thiết cho việc quản lý user
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100)) # Chiều dài tối đa 100 (Tên hiển thị trong ứng dụng)
  username = db.Column(db.String(100), nullable=False) # (Tên để đăng nhập)
  password_hashed = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100))
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  is_admin = db.Column(db.Boolean, default=False)
  # unique = True để đảm bảo không có 2 user nào trùng cả username và email
  db.UniqueConstraint(username, email)

  # Decorator này dùng để tạo ra một thuộc tính giả
  @property
  def password(self):
    if self.password_hashed is not None:
      return None
    return self.password

  @password.setter
  def password(self, password):
    # Hàm này được sử dụng để mã hóa password
    # :param password:
    # :return:
    self.password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

  # Cách sử dụng: 
  # khi đọc user.password thì sẽ trả về None nếu password_hashed 
  # khi gán user.password = 'my_password' thì nó sẽ được tự động mã hóa vào lưu vào password_hashed 

  def check_password_correction(self, attempted_password):
    # Hàm này được sử dụng để kiểm tra password đã được mã hóa có khớp với password người dùng nhập vào hay không 
    # :param attempted_password: 
    # :return: 
    return bcrypt.check_password_hash(self.password_hashed, attempted_password)

  def __repr__(self):
    return '<User %r>' % self.username
  
class Project(db.Model):
  __tablename__ = 'project'
  id = db.Column(db.Integer, primary_key=True)  
  name = db.Column(db.String(255))
  description = db.Column(db.Text)
  status = db.Column(db.String(100))
  active = db.Column(db.Boolean, default=True)
  sequence = db.Column(db.Integer)
  manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  date_start = db.Column(db.Date)
  date_end = db.Column(db.Date)
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  create_uid = db.Column(db.Integer, default=0)
  write_uid = db.Column(db.Integer, default=0)
  tasks = db.relationship('Task', backref='project')
  # backref để tạo ra một thuộc tính ảo trong class Task để lấy ra thông tin của project
  progress = db.Column(db.Float)

  def __repr__(self):
    return '<Project %r>' % self.name
  
class Task(db.Model):
  __tablename__ = 'task'
  id: int
  name: str
  description: str
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  status = db.Column(db.String(100))
  name = db.Column(db.String(255))
  description = db.Column(db.Text)
  active = db.Column(db.Boolean, default=True)
  priority = db.Column(db.Integer)
  sequence = db.Column(db.Integer)
  date_start = db.Column(db.Date)
  date_end = db.Column(db.Date)
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

  def __repr__(self):
    return '<Task %r>' % self.name