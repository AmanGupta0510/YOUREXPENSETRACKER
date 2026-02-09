from expenseTracker import db,login_manager
from expenseTracker import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(),nullable=False,primary_key = True)
    username = db.Column(db.String(length=30),nullable=False)
    password_hash = db.Column(db.String(length=128),nullable=False)
    email_address = db.Column(db.String(length=50),nullable=False)
   
    expenses = db.relationship("Expense",back_populates='user',lazy=True)
    
    # lazy=True = "Load related data only when accessed" (default, fast).
    # Without it: Loads everything immediately (slow).

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plainTextPassword):
        self.password_hash = bcrypt.generate_password_hash(plainTextPassword).decode('utf-8') #convert the plain password into human readable hex code.using bcrypt.generate_password_hash() func and set it into user db password column 

    def passwordChecker(self,attemptedPassword):#check whether the user provided password is equal to user saved password in db.
        return bcrypt.check_password_hash(self.password_hash,attemptedPassword) 


    




class Expense(db.Model):
    __tablename__ = 'expense'
   
    id = db.Column(db.Integer(),primary_key = True,nullable=False)
    category_name = db.Column(db.String(length=30),nullable=False)
    item_name = db.Column(db.String(length=30),nullable=False)
    quantity = db.Column(db.Float(),nullable=False , default=0)
    price = db.Column(db.Float(),nullable=False,default=0)
    total = db.Column(db.Float(),nullable=False,default=0)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='expenses',lazy=True)


    
    def to_dict(self):
        return {
                'category_name':self.category_name,
                'item_name' :self.item_name,
                'quantity' : self.quantity,
                'price':self.price,
                'total':self.total
            }
        

