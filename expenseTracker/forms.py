from flask_wtf import FlaskForm,CSRFProtect
from wtforms import DateField, DecimalField, IntegerField, StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import Length ,EqualTo,DataRequired,ValidationError,Email
from expenseTracker.models import User
from expenseTracker import app
csrf=CSRFProtect(app)


class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('Username is already exists!')
    def validate_emailadd(self,email_to_check):
        email_address = User.query.filter_by(email_address=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address is already exists!') 

    # the above method are from flask FlaskForm and triggering out those method are handle by flask form itself and FlaskForm automatically triggers custom validate_{fieldname}() methods during form.validate_on_submit().        
    username = StringField(label='User Name',validators=[DataRequired(),Length(min=2, max=20)])
    email_address = StringField(label='Email Address',validators=[DataRequired(),Email()])
    password1 = PasswordField(label='Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='User Name',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class AddItems(FlaskForm):
     
    category = SelectField('Choose Category',
                            choices=[
                               ('','Select one'),
                               ('fastfood','FastFoods'),
                               ('stationery','Stationerys'),
                               ('wearable','Wearables') ,
                               ('other','Others'),
                               ('grocerie','Groceries'),
                               ('beverage','Beverages')
                            ]
                        )
    item = StringField(label='Item',validators=[DataRequired(),Length(min=4,max=10)])
    quantity = IntegerField(label='Quantity',validators=[DataRequired()])
    price = DecimalField(label='Price',validators=[DataRequired()])

    save = SubmitField(label='Save')
    delete = SubmitField(label='Delete')
                              
