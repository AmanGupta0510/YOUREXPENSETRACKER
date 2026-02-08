from operator import and_
from flask import jsonify, redirect, render_template,url_for,flash,request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from expenseTracker import app,db
from expenseTracker.forms import AddItems, LoginForm,RegisterForm
from expenseTracker.models import Expense, User
from flask_login import current_user, login_required, login_user,logout_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')  

@app.route('/register',methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template('register.html',form=form)
@app.route('/register',methods=["POST"])
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
        return jsonify({'success': True})
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f"There was an error while creating user:{err_msg}",category='danger')
    return jsonify({'error': 'Invalid form'}), 400
    


@app.route('/login',methods=["GET","POST"]) 
def login_page():
    form = LoginForm()
    # When you write form = LoginForm():
    # GET request: flask.request.form = empty → form.username.data = None
    # POST request: flask.request.form = {'username': 'bob', 'password': '123'} → Flask-WTF automatically fills:
      
    return render_template('login.html',form=form)



@app.route('/api/login', methods=['POST'])
@cross_origin()
def api_login():
    # 1. Get raw JSON - NO FORM VALIDATION
    data = request.get_json()
    
    # 2. SAFETY CHECKS FIRST
    print("Raw data received:", data)  # Debug line
    
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    # 3. Now safe to query
    attempted_user = User.query.filter_by(username=data.get('username')).first()
    
    if attempted_user and attempted_user.passwordChecker(attemptedPassword=data.get('password')):
        login_user(attempted_user)
        
        
        token = create_access_token(identity=str(attempted_user.id))
        print(f"Login SUCCESS for {attempted_user.username}")  # Debug
        return jsonify({"accessToken": token})
    else:
        print("Login FAILED - invalid credentials")  # Debug
        return jsonify({'error': 'Invalid credentials'}), 401
    

@app.route('/logout',methods=["GET","POST"])
def logout_page():
    logout_user()
    flash(f'You have been logged out!',category = 'info')
    return redirect(url_for('home_page'))

@app.route('/add-expense')
@cross_origin()
def operation_page():
    form = AddItems()
    return render_template('operation.html',form=form)     
        
@app.route('/api/add-expense', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()

def add_expense():

    if request.method == 'OPTIONS':
       return '', 200
    
    data = request.get_json()
    print(data)
    items = Expense.query.filter_by(item_name=data.get('item'),price=data.get('price')).first()
    quantity = int(data.get('quantity') or 0)
    price = int(data.get('price') or 0)
    if items:
        items.quantity+=quantity
        items.total = price*items.quantity
    else:
        items = Expense(
                            category_name=data.get('category'),
                            item_name = data.get('item'),
                            quantity = data.get('quantity'),
                            price = data.get('price'),
                            total = quantity*price,
                            user_id = current_user.id
                        )     
            
        db.session.add(items)
        db.session.commit()
    current_user_id = get_jwt_identity()    
    curr_expenses = db.session.query(Expense).filter(Expense.user_id==int(current_user_id)).all()  
    return jsonify( [ ex.to_dict() for ex in curr_expenses ] )

@app.route('/api/expenses', methods=['GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def get_expense():
    
    if request.method == 'OPTIONS':
        return '', 200
    current_user_id = get_jwt_identity()
    expected_expense = db.session.query(Expense).filter(Expense.user_id==int(current_user_id)).all()
    return jsonify([expense.to_dict() for expense in expected_expense])


    


   




