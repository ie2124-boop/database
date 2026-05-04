# CSCI-UA.0060 Final Exam Cheat Sheet

---

## SQLITE DATA TYPES
```
INTEGER   whole numbers        employeeId, orderId, quantity
REAL      decimals             priceEach, creditLimit, buyPrice
TEXT      strings & dates      customerName, orderDate, status
NULL      missing value        shippedDate before shipped
BLOB      binary               (rarely used)

CHECK constraint:
  status TEXT CHECK(status IN ('Shipped','In Process','Cancelled'))
```

---

## DDL — CREATE / ALTER / DROP
```sql
-- Create table
CREATE TABLE employee (
  employeeId   INTEGER  PRIMARY KEY,
  lastName     TEXT     NOT NULL,
  officeCode   TEXT     NOT NULL,
  reportsTo    INTEGER,                          -- self-ref FK (nullable)
  creditLimit  REAL     DEFAULT 0.0,
  status       TEXT     CHECK(status IN ('Active','Inactive')),
  FOREIGN KEY (officeCode)  REFERENCES office(officeCode),
  FOREIGN KEY (reportsTo)   REFERENCES employee(employeeId)
);

-- Add a column
ALTER TABLE office ADD COLUMN territory TEXT;

-- Drop table safely
DROP TABLE IF EXISTS temp_data;
```

---

## DML — INSERT / UPDATE / DELETE
```sql
-- Insert one row
INSERT INTO office (officeCode, city, country)
VALUES ('7', 'Tokyo', 'Japan');

-- Insert multiple rows
INSERT INTO employee (employeeId, lastName, firstName, officeCode, jobTitle)
VALUES
  (2001, 'Tanaka', 'Hiro', '1', 'Sales Rep'),
  (2002, 'Kim',    'Soo',  '4', 'Sales Rep');

-- Update (ALWAYS use WHERE)
UPDATE orders
SET status = 'Shipped', shippedDate = '2003-01-15'
WHERE orderId = 10100;

-- Update with arithmetic
UPDATE customer SET creditLimit = creditLimit * 1.20 WHERE customerId = 114;
UPDATE product  SET quantityInStock = quantityInStock - 30 WHERE productId = 'S10_1678';

-- Delete — child rows first, then parent
DELETE FROM orderdetails WHERE orderId = 10100;
DELETE FROM orders      WHERE customerId = 103;
DELETE FROM customer    WHERE customerId = 103;
```

---

## DQL — SELECT & WHERE
```sql
-- Basic
SELECT productName, productLine, MSRP FROM product;
SELECT * FROM customer WHERE country = 'France';

-- Comparisons
WHERE creditLimit > 100000
WHERE creditLimit BETWEEN 50000 AND 100000   -- inclusive both ends
WHERE shippedDate IS NULL                    -- NOT: = NULL
WHERE shippedDate IS NOT NULL
WHERE country IN ('France', 'Spain', 'USA')
WHERE country NOT IN ('USA', 'Australia')

-- LIKE patterns
WHERE productName LIKE '%Harley%'   -- contains
WHERE productName LIKE 'S10_%'      -- starts with S10 + at least 1 char
WHERE productName NOT LIKE '%Ferrari%'

-- AND / OR (parentheses matter!)
WHERE (country = 'USA' OR country = 'France') AND creditLimit > 80000

-- Date filter for a year
WHERE orderDate BETWEEN '2003-01-01' AND '2003-12-31'
```

---

## JOINS
```sql
-- INNER JOIN — only matching rows (most common)
SELECT o.orderId, c.customerName
FROM   orders o
JOIN   customer c ON o.customerId = c.customerId;

-- LEFT JOIN — all left rows, NULL if no match on right
SELECT c.customerName, o.orderId
FROM   customer c
LEFT JOIN orders o ON c.customerId = o.customerId;

-- Customers with NO orders (classic exam pattern)
SELECT c.customerName, c.country
FROM   customer c
LEFT JOIN orders o ON c.customerId = o.customerId
WHERE  o.orderId IS NULL;

-- 3-table chain: office → employee → customer
SELECT of.city, e.lastName, c.customerName
FROM   office of
JOIN   employee e ON of.officeCode  = e.officeCode
JOIN   customer c ON e.employeeId   = c.salesRepEmployeeNumber;

-- 4-table chain: employee → customer → orders → orderdetails
SELECT e.lastName, c.customerName, o.orderId, od.productId,
       od.quantityOrdered * od.priceEach AS lineRevenue
FROM   employee e
JOIN   customer     c  ON e.employeeId  = c.salesRepEmployeeNumber
JOIN   orders       o  ON c.customerId  = o.customerId
JOIN   orderdetails od ON o.orderId     = od.orderId;
```

---

## AGGREGATE FUNCTIONS + GROUP BY
```sql
-- Functions
COUNT(*)              -- count all rows
COUNT(col)            -- count non-NULL values
SUM(col)              -- total
AVG(col)              -- average
MIN(col) / MAX(col)   -- smallest / largest
ROUND(AVG(col), 2)    -- round to 2 decimal places

-- GROUP BY pattern
SELECT   country, COUNT(*) AS customerCount
FROM     customer
GROUP BY country;

-- GROUP BY + JOIN (most exam questions)
SELECT   p.productLine,
         SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM     orderdetails od
JOIN     product p ON od.productId = p.productId
GROUP BY p.productLine;

-- HAVING — filter AFTER aggregation (not WHERE)
SELECT   productLine, AVG(buyPrice) AS avgPrice
FROM     product
GROUP BY productLine
HAVING   AVG(buyPrice) > 60.00;

-- "Which X has the MOST Y" — full pattern
SELECT   e.lastName, e.firstName,
         SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM     employee e
JOIN     customer     c  ON e.employeeId  = c.salesRepEmployeeNumber
JOIN     orders       o  ON c.customerId  = o.customerId
JOIN     orderdetails od ON o.orderId     = od.orderId
WHERE    o.orderDate BETWEEN '2003-01-01' AND '2003-12-31'
GROUP BY e.employeeId, e.lastName, e.firstName
ORDER BY totalRevenue DESC   -- ASC for LEAST
LIMIT    1;

-- COUNT(DISTINCT) — avoid double-counting across joins
SELECT of.city, COUNT(DISTINCT c.customerId) AS customerCount
FROM   office of
JOIN   employee e ON of.officeCode = e.officeCode
JOIN   customer c ON e.employeeId  = c.salesRepEmployeeNumber
GROUP BY of.officeCode, of.city
ORDER BY customerCount DESC
LIMIT 1;
```

---

## SUBQUERIES
```sql
-- Single value (use =)
SELECT productName, buyPrice
FROM   product
WHERE  buyPrice > (SELECT AVG(buyPrice) FROM product);

-- Multiple values (use IN)
SELECT customerName
FROM   customer
WHERE  customerId IN (
  SELECT customerId FROM orders WHERE status = 'Cancelled'
);

-- Customers with NO orders (alternative to LEFT JOIN)
SELECT customerName
FROM   customer
WHERE  customerId NOT IN (SELECT customerId FROM orders);
```

---

## QUERY CLAUSE ORDER (always in this order)
```
SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
```

---

## PYTHON — SQLite
```python
import sqlite3

# Connect + cursor
conn   = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Parameterized query — ALWAYS use ? not string concat
cursor.execute("SELECT * FROM flights WHERE toAirport = ?", ('JFK',))
results = cursor.fetchall()    # list of all rows
row     = cursor.fetchone()    # just the first row

# Two parameters
cursor.execute(
    "SELECT * FROM flights WHERE toAirport = ? AND date = ?",
    ('JFK', '2024-05-01')
)

# Access results
for row in results:
    print(row[0], row[1])     # row is a tuple — index by position

# INSERT/UPDATE/DELETE needs commit
cursor.execute("INSERT INTO flights (toAirport) VALUES (?)", ('JFK',))
conn.commit()
```

---

## FLASK — Routes, GET, POST
```python
from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- URL PARAMETER (data in the route itself) ---
@app.route('/orders/<customerId>')
def get_orders(customerId):           # Flask passes it as function arg
    conn   = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE customerId = ?", (customerId,))
    results = cursor.fetchall()
    return render_template('orders.html', orders=results)

# --- GET (data in URL: /search?airport=JFK) ---
@app.route('/search')                 # GET is default — methods=['GET'] optional
def search():
    airport = request.args.get('airport')   # reads ?airport=JFK
    return render_template('results.html', airport=airport)

# --- POST (data hidden in form body) ---
@app.route('/newFlight', methods=['POST'])
def new_flight():
    fromAirport = request.form['fromAirport']   # reads form field
    toAirport   = request.form['toAirport']
    cursor.execute(
        "INSERT INTO flights (fromAirport, toAirport) VALUES (?, ?)",
        (fromAirport, toAirport)
    )
    conn.commit()
    return redirect(url_for('displayFlights'))  # function name, not URL

# --- GET + POST on same route ---
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        airport = request.form['airport']
        return render_template('results.html', airport=airport)
    return render_template('search.html')       # GET — just show the form
```

---

## JINJA2 TEMPLATES
```html
<!-- Display a variable -->
{{ variable }}
{{ flight.toAirport }}

<!-- For loop -->
{% for order in orders %}
  {{ order[0] }} — {{ order[1] }}
{% endfor %}

<!-- If statement -->
{% if flight.toAirport == 'JFK' %}
  {{ flight.flightNumber }}
{% endif %}

{% if customer.creditLimit > 100000 %}
  VIP Customer
{% else %}
  Standard Customer
{% endif %}

<!-- Extend a base template -->
{% extends "base.html" %}
{% block content %}
  page content here
{% endblock %}
```

---

## MONGODB / MONGITA
```python
from mongita import MongitaClientDisk

# Connect
client  = MongitaClientDisk("mongita_data")
db      = client.student_db
orders  = db.orders              # collection (= table)

# Find one
orders.find_one()                              # first doc
orders.find_one({"toAirport": "JFK"})         # with filter

# Find many
all_orders  = list(orders.find())
jfk_orders  = list(orders.find({"toAirport": "JFK"}))
limited     = orders.find().limit(3)

# Comparison operators
orders.find({"shippedDate": {"$gt": "2004-01-01"}})   # greater than
orders.find({"amount":      {"$lt": 500}})             # less than
orders.find({"amount":      {"$gte": 100}})            # >=
orders.find({"amount":      {"$lte": 999}})            # <=

# Count
orders.count_documents({})                    # all
orders.count_documents({"toAirport": "JFK"}) # filtered

# Store in variable (your exam Q9)
trip = orders.find_one({"toAirport": "JFK"})
lateOrders = orders.find({"shippedDate": {"$gt": "2004-01-01"}})
```

---

## CARS DB — FK CHAIN (memorize this)
```
office ──── employee ──── customer ──── orders ──── orderdetails ──── product
         officeCode    salesRepEmpNum  customerId    orderId          productId
         = officeCode  = employeeId   = customerId  = orderId        = productId

Self-join: employee.reportsTo → employee.employeeId  (boss is also an employee)
```

---

## COMMON EXAM PATTERNS

**How many X have no Y?**
```sql
SELECT COUNT(*) FROM customer c
LEFT JOIN orders o ON c.customerId = o.customerId
WHERE o.orderId IS NULL;
```

**Which X has the most/least Y?**
```sql
GROUP BY x ORDER BY COUNT(*) DESC LIMIT 1;   -- most
GROUP BY x ORDER BY COUNT(*) ASC  LIMIT 1;   -- least
```

**Revenue in a specific year?**
```sql
WHERE orderDate BETWEEN '2003-01-01' AND '2003-12-31'
SUM(od.quantityOrdered * od.priceEach) AS revenue
```

**Products never ordered?**
```sql
WHERE productId NOT IN (SELECT productId FROM orderdetails)
```

**WHERE vs HAVING**
```
WHERE  → filters rows   → before GROUP BY  → cannot use aggregates
HAVING → filters groups → after  GROUP BY  → must use aggregates
```

**NULL rules**
```
= NULL    ✗ WRONG — always returns nothing
IS NULL   ✓ CORRECT
IS NOT NULL ✓ CORRECT
```

**Tuple with one value — trailing comma is required**
```python
cursor.execute("... WHERE x = ?", ('JFK',))   # ✓ ('JFK',) is a tuple
cursor.execute("... WHERE x = ?", ('JFK'))    # ✗ ('JFK') is just a string
```
