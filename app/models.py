from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Staff(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'staffs'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(5), db.ForeignKey('staff_roles.id'))
    f_name = db.Column(db.String(60), index=True, nullable=False)
    l_name = db.Column(db.String(60), index=True,  nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15), index=True)
    email = db.Column(db.String(60), index=True, nullable=False)
    entry_date = db.Column(db.Date, index=True)
    partner_givings = db.relationship('PartnerGiving', backref='staff',
                                lazy='dynamic')
    tithe_givings = db.relationship('TitheGiving', backref='staff',
                                lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Staff: {}>'.format(self.f_name +" "+ self.l_name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))


class Staff_Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'staff_roles'

    id = db.Column(db.String(5), primary_key=True)
    role = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))
    entry_date = db.Column(db.Date, index=True)
    staffs = db.relationship('Staff', backref='staff_role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Staff Role: {}>'.format(self.role)

class Group(db.Model):
    """
    Create a Group table
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(60), unique=True, nullable=False)
    entry_date = db.Column(db.Date, index=True)
    churches = db.relationship('Church', backref='group',
                                lazy='dynamic')
    members = db.relationship('Member', backref='group',
                                lazy='dynamic')

    def __repr__(self):
        return '<Group: {}>'.format(self.group)


class Church(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'churches'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    church = db.Column(db.String(60), nullable=False)
    entry_date = db.Column(db.Date, index=True)
    members = db.relationship('Member', backref='church',
                                lazy='dynamic')


    def __repr__(self):
        return '<Church: {}>'.format(self.church)


class Pcf(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'pcfs'

    id = db.Column(db.Integer, primary_key=True)
    pcf = db.Column(db.String(60), nullable=False)
    entry_date = db.Column(db.Date, index=True)
    cells = db.relationship('Cell', backref='pcf',
                                lazy='dynamic')
    members = db.relationship('Member', backref='pcf',
                                lazy='dynamic')

    def __repr__(self):
        return '<PCF: {}>'.format(self.pcf)

class Cell(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'cells'

    id = db.Column(db.Integer, primary_key=True)
    pcf_id = db.Column(db.Integer, db.ForeignKey('pcfs.id'))
    cell = db.Column(db.String(60), nullable=False)
    entry_date = db.Column(db.Date, index=True)
    members = db.relationship('Member', backref='cell',
                                lazy='dynamic')

    def __repr__(self):
        return '<PCF: {}>'.format(self.pcf)

class Member(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    church_id = db.Column(db.Integer, db.ForeignKey('churches.id'))
    pcf_id = db.Column(db.Integer, db.ForeignKey('pcfs.id'))
    cell_id = db.Column(db.Integer, db.ForeignKey('cells.id'))
    title = db.Column(db.String(60), nullable=True)
    l_name = db.Column(db.String(60), index=True,  nullable=False)
    f_name = db.Column(db.String(60), index=True, nullable=False)
    phone = db.Column(db.String(15), index=True)
    email = db.Column(db.String(60), index=True)
    kingschat_no = db.Column(db.String(60))
    birthday = db.Column(db.String(60))
    w_anniversary = db.Column(db.String(60))
    entry_date = db.Column(db.Date, index=True)
    partner_givings = db.relationship('PartnerGiving', backref='member',
                                lazy='dynamic')
    tithe_givings = db.relationship('TitheGiving', backref='member',
                                lazy='dynamic')

    def __repr__(self):
        return '<Member: {}>'.format(self.f_name + self.l_name)

class PartnershipArm(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'partnership_arms'

    id = db.Column(db.Integer, primary_key=True)
    partnership_arm = db.Column(db.String(100), nullable=False)
    entry_date = db.Column(db.Date, index=True)
    partner_givings = db.relationship('PartnerGiving', backref='partner_arm',
                                lazy='dynamic')

    def __repr__(self):
        return '<Arm: {}>'.format(self.partnership_arm)

class PartnerGiving(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'partner_givings'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    arm_id = db.Column(db.Integer, db.ForeignKey('partnership_arms.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    is_pledge = db.Column(db.Boolean, default=False)
    entry_date = db.Column(db.Date)

    def __repr__(self):
        return '<Partner Giving: {}>'.format(self.amount)

class TitheGiving(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'tithe_givings'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    entry_date = db.Column(db.Date, index=True)

    def __repr__(self):
        return '<TitheGiving: {}>'.format(self.amount)
