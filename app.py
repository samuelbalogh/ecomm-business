import sqlite3
import datetime
import json

from flask import Flask, Response

app = Flask(__name__)

# TODO get commission data
SQL_SELECT_REPORT_FOR_DATE = """
    WITH order_totals AS (
        SELECT order_id, SUM(order_lines.total_amount) AS order_total FROM order_lines GROUP BY order_id
    ),
    commissions_per_order AS (
        SELECT
          commissions.date,
          SUM(commissions.rate) / COUNT(orders.id)
        FROM commissions, orders
        WHERE commissions.date = date(orders.created_at)
        GROUP BY
          commissions.date
    )
    SELECT
        SUM(order_lines.quantity) AS items,
        COUNT(orders.customer_id) AS customers,
        SUM(order_lines.discounted_amount) AS total_discount_amount,
        AVG(order_lines.discount_rate) AS discount_rate_avg,
        AVG(order_totals.order_total) AS order_total_avg,
        SUM(commissions.rate) AS total_commission
    FROM
        orders, order_lines, order_totals, commissions, commissions_per_order
    WHERE
        orders.id = order_lines.order_id AND
        order_totals.order_id = orders.id  AND
        date(orders.created_at) = ? AND
        commissions.date = date(orders.created_at) AND
        commissions_per_order.date = date(orders.created_at)
"""


@app.route('/<date>')
def report(date):
    con = sqlite3.connect('ecomm.db')
    cur = con.cursor()

    try:
        # TODO better way of ensuring date format
        datetime.date.fromisoformat(date)
    except ValueError:
        # TODO logging
        return Response("Invalid date", status=400)

    row = cur.execute(SQL_SELECT_REPORT_FOR_DATE, (date,)).fetchone()
    field_names = [description[0] for description in cur.description]

    results = [i for i in zip(field_names, row)]

    return Response(
        json.dumps(dict(results)),
        content_type='application/json'  # TODO how to set this automatically
    )


if __name__ == '__main__':
    app.run()
