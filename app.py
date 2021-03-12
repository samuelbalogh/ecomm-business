import sqlite3

from flask import Flask

app = Flask(__name__)

SQL_SELECT_REPORT_FOR_DATE = """
    WITH order_totals AS (
        SELECT order_id, SUM(order_lines.total_amount) FROM order_lines GROUP BY order_id
    ),
    commissions_per_order AS (

    
    )
    SELECT
        SUM(order_lines.quantity) AS nr_items_sold,
        COUNT(orders.customer_id) AS nr_customers,
        SUM(order_lines.discounted_amount) AS total_discount,
        AVG(order_lines.discounted_amount) AS avg_discount,
        AVG(order_totals) AS avg_order_total,
        SUM(commissions.rate) AS total_commission
    FROM
        orders, order_lines, order_totals, commissions
    WHERE
        orders.id = order_lines.order_id AND
        order_totals.order_id = orders.id AND
        orders.created_at = ? AND
        commissions.date = ?

"""


@app.route('/<date>')
def report(date):
    con = sqlite3.connect('ecomm.db')
    cur = con.cursor()

    return 'report'


if __name__ == '__main__':
    app.run()
