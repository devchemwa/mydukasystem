from flask import Flask,render_template,request,url_for,redirect,flash,session
from dbservice import fetch_data,insert_data,insert_sale,profit,sales,day_sales,newUser,check_email
from flask_bcrypt import Bcrypt
# creating an instance of Flask class:
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
bcrypt = Bcrypt(app)
# route:
# @app.route("/")
# def hello():
#     return "Hello, World!"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/product")
def get_products():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log'))
    prods = fetch_data('products')
    return render_template('product.html', p = prods)

@app.route('/sale')
def get_sales():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log'))
    s = fetch_data('sales')
    p = fetch_data('products')
    return render_template('sales.html', sa = s, p = p)


@app.route('/add_user', methods =['POST','GET'])
def addUser():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log'))
    if request.method =='POST':
       firstName = request.form['first_name']
       lastName = request.form['last_name']
       mail = request.form['email']
       password = request.form['password']
       hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       correct  = check_email(mail)
       if correct == None:
            new_user = (firstName,lastName,mail,hashed_password)
            newUser(new_user)
            return(redirect(url_for('log')))
       else:
            flash("email exists already") 
            return redirect(url_for('log'))


@app.route('/dashboard')
def dash():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log')) 
    profitPerproduct = profit()
    salesPerproduct = sales()
    pName = []
    proffit = []
    salePerproduct = []
    productSale = []
    for i in profitPerproduct:
        pName.append(i[0])
        proffit.append(float(i[1]))
    for a in salesPerproduct:
        salePerproduct.append(a[0])
        productSale.append(float(a[1]))    


    day_sale = day_sales()
    dSale = []
    date = []
    for i in day_sale:
        dSale.append(float(i[1]))
        date.append(str(i[0]))      
   
    return render_template('dashboard.html', pName = pName, proffit = proffit, productSale = productSale, salePerproduct = salePerproduct, dSale = dSale, date = date) 
# running the application

# all html files are placed in the templates folder
# all css and javascript are placed inside the static folder

# create html files for each route (products.html), (sales.html), (dashborard.html), (home.html)


@app.route('/add_product', methods=['POST','GET'])
def addProduct():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log'))
    if request.method == 'POST':
        prodName = request.form['productName']
        bPrice = request.form['buyingPrice']
        sPrice = request.form['sellingPrice']
        sQuantity = request.form['stockQuantity']

        p = (prodName,bPrice,sPrice,sQuantity)
        insert_data(p)
        return redirect(url_for('get_products'))
    
@app.route('/make_sale', methods = ['POST', 'GET'])
def makeSale():
    if 'email' not in session:
        flash("login to access this page")
        return redirect(url_for('log')) 
    if request.method == 'POST':
        pid = request.form['pid']
        quantity = request.form['quantity']

        newSale = (pid,quantity)
        insert_sale(newSale)
        return redirect(url_for('get_sales'))
    
@app.route('/login', methods = ['POST', 'GET'])
def log():
    if request.method == 'POST':
        mail = request.form['email']
        session['email'] = mail
        passwaad = request.form['password']
        user = check_email(mail)
        if user == None:
            flash("user doesn't exist")
            return redirect(url_for('addUser'))
        else:
            if bcrypt.check_password_hash(user[-1], passwaad):
                flash("Login successfull") 
                return redirect(url_for('dash'))
            else:
               flash('wrong password')
    return render_template('login.html')

@app.route('/logout')
def log_out():
    session.pop('email', None)
    return redirect(url_for('log'))
app.run(debug = True) 