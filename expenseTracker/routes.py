from operator import and_
from flask import jsonify, redirect, render_template,url_for,flash,request
from expenseTracker import app,db
from expenseTracker.forms import AddItems, LoginForm,RegisterForm
from expenseTracker.models import Expense, User
from flask_login import current_user, login_required, login_user,logout_user
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity 
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')  

@app.route('/register',methods=["GET","POST"])
def register_page():
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            password=form.password1.data,
                            email_address=form.email_address.data)
        print(form.username.data)  
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}",category='success')
        return redirect(url_for('operation_page'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f"There was an error while creating user:{err_msg}",category='danger')
    return  render_template('register.html',form=form)
    


@app.route('/login',methods=["GET","POST"]) 
def login_page():
    form = LoginForm()
    # When you write form = LoginForm():
    # GET request: flask.request.form = empty → form.username.data = None
    # POST request: flask.request.form = {'username': 'bob', 'password': '123'} → Flask-WTF automatically fills:

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.passwordChecker(attemptedPassword = form.password.data):
            login_user(attempted_user)
            # access_token = create_access_token(identity=attempted_user.id)
            flash(f'Success! You are logged in as { attempted_user.username }',category='success')
            return redirect(url_for('operation_page' ))
        else:
            flash(f'Username or password are not match! try again',category='danger')

    return render_template('login.html',form=form)



@app.route('/logout',methods=["GET","POST"])
def logout_page():
    logout_user()
    flash(f'You have been logged out!',category = 'info')
    return render_template('home.html')

@app.route('/add-expense')
@login_required
def operation_page():
    form = AddItems()
    return render_template('operation.html',form=form)     
        
@app.route('/api/add-expense',methods=["POST"])
@jwt_required()
def add_expense():
    form = AddItems()
    
    data = request.get_json()
    print(data)
    items = AddItems.query.filter_by(and_(item_name=form.item.data,price=form.price.data)).first()
    quantity = int(form.quantity.data or 0)
    price = int(form.price.data or 0)
    if items:
        items.quantity+=quantity
        items.total = price*items.quantity
    else:
        items = Expense(
                            category_name=form.category.data,
                            item_name = form.item.data,
                            quantity = form.quantity.data,
                            price = form.price.data,
                            total = quantity*price,
                            user_d = current_user.id
                        )     
            
        db.session.add(items)
        db.session.commit()
    current_user_id = get_jwt_identity()    
    curr_expenses = db.session.query(Expense).filter(Expense.user_id==current_user_id).all()  
    return jsonify( [ ex.to_dict() for ex in curr_expenses ] )

@app.route('/api/expenses')
@jwt_required()
def get_expense():
    current_user_id = get_jwt_identity()
    expected_expense = db.session.query(Expense).filter(Expense.user_id==current_user_id).all()
    return jsonify([expense.to_dict() for expense in expected_expense])



    


   




