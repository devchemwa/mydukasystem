import psycopg2
conn = psycopg2.connect( 
    host='localhost',
    dbname = 'myduka',
    password = '1234',
    user = 'postgres',
    port = 5432
      )

#CREATING  A CURSOR:
cur = conn.cursor()

# fetching data from the database:
def fetch_data(a):
    query = (f"SELECT * FROM {a};")
    cur.execute(query)
    prods = cur.fetchall() 
    return prods



# print(prods)


# write a query to insert products:
def insert_data(a):
 query = "INSERT INTO products(name,buying_price,selling_price,stock_quantity) VALUES (%s,%s,%s,%s);"
 cur.execute(query,a)
 conn.commit()

# insert_data(('Unga',100,150,200))

# write a query to insert sales:
def insert_sale(b):
 query = "insert into sales(pid,quantity,created_at) values(%s,%s,now());"
 cur.execute(query,b)
 conn.commit()

# print(y)

# write a query and a function to:
# get profit per product
def profit():
  query = 'SELECT products.name, SUM((selling_price - buying_price) * sales.quantity) AS profit from products inner join sales on products.id=sales.id group by name order by SUM((selling_price - buying_price) * sales.quantity) asc;'
  p = cur.execute(query)
  p = cur.fetchall()
  return p

# print(profits)  
# get sales per product
def sales():
  query  = 'SELECT products.name, SUM(products.selling_price * sales.quantity) AS spp FROM sales INNER JOIN products ON sales.id=products.id GROUP BY products.name;'
  cur.execute(query)
  salee = cur.fetchall()
  return salee

# print(s)

# get sales per day
def day_sales():
 query = 'SELECT created_at, SUM(products.selling_price * sales.quantity) AS sales FROM sales INNER JOIN products ON sales.id=products.id GROUP BY sales.created_at;'
 cur.execute(query)
 sale = cur.fetchall()
 return sale

# print(day)

# get profit per day
def day_profit():
  query = 'select name, created_at, SUM((selling_price - buying_price) * quantity) AS profit FROM products INNER JOIN sales ON products.id=sales.id GROUP BY created_at, name ORDER BY SUM((selling_price - buying_price) * quantity) DESC;'
  cur.execute(query)
  profit_day = cur.fetchall()
  return profit_day 
 

def newUser(z):
  query = 'insert into customers(first_name,last_name,email,password) values(%s,%s,%s,%s);'
  cur.execute(query, z)
  conn.commit()

def check_email(m):
  query = "select * from customers where email = %s"
  cur.execute(query, (m,))
  data = cur.fetchone()
  if data:
    return data