# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1=first,last name and job title of employees working in Boston.
df_boston = pd.read_sql("""
    SELECT (e.firstName || ' ' || e.lastName) AS name, e.jobTitle
    FROM employees e
    INNER JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
""", conn)

# STEP 3
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName ASC, e.lastName ASC;
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName ASC;
""", conn)

# STEP 5
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    INNER JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
    FROM employees e
    INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC;
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM products p
    INNER JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC;
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    INNER JOIN orderdetails od ON p.productCode = od.productCode
    INNER JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
df_customers = pd.read_sql("""
    SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
    FROM offices o
    INNER JOIN employees e ON o.officeCode = e.officeCode
    INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city;
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
    SELECT DISTINCT 
        e.employeeNumber, 
        e.firstName, 
        e.lastName, 
        off.city, 
        off.officeCode
    FROM employees e
    INNER JOIN offices off ON e.officeCode = off.officeCode
    INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    INNER JOIN orders o ON c.customerNumber = o.customerNumber
    INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        INNER JOIN orders o2 ON od2.orderNumber = o2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    );
""", conn)
conn.close()