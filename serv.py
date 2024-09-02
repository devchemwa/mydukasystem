import psycopg2

# connect to database:
conn = psycopg2.connect(
    host='localhost',
    dbname = 'myduka',
    password = '1234',
    user = 'postgres',
    port = 5432
)

# declaring a cursor to perform database operations:
curr = conn.cursor()
# get products:
def get_prods():
    curr.execute('SELECT * FROM products')
    products = curr.fetchall()
    return products

prods = get_prods()
for i in prods:
    print(i)

# get sales
def get_sales():
    curr.execute('SELECT * FROM sales')
    sales = curr.fetchall()
    return sales

sales = get_sales()
print(sales)

