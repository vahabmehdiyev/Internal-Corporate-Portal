from config.database import db

class IPAddress(db.Model):
    __tablename__ = 'ip_addresses'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(255), unique=True, nullable=False)
    note = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Access(db.Model):
    __tablename__ = 'accesses'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    # Many-to-Many connection with User
    users = db.relationship('User', secondary='user_accesses', back_populates='accesses')


