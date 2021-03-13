import sqlite3
import datetime
import json

from flask import Flask

app = Flask(__name__)

DB_NAME = 'ecomm.db'

# NOTE: commission per promotion data is missing due to lack of time
SQL_SELECT_REPORT_FOR_DATE = """
    WITH order_totals AS (
        SELECT order_id, SUM(order_lines.total_amount) AS order_total FROM order_lines GROUP BY order_id
    ),
    commissions_per_order AS (
        SELECT
          commissions.date,
          SUM(commissions.rate) / COUNT(orders.id) AS commission_per_order
        FROM commissions, orders
        WHERE commissions.date = date(orders.created_at)
        GROUP BY
          commissions.date
    )
    SELECT
        SUM(order_lines.quantity) AS items,
        COUNT(DISTINCT orders.customer_id) AS customers,
        SUM(order_lines.discounted_amount) AS total_discount_amount,
        AVG(order_lines.discount_rate) AS discount_rate_avg,
        AVG(order_totals.order_total) AS order_total_avg,
        SUM(commissions.rate) AS total_commission,
        commissions_per_order.commission_per_order AS order_average
    FROM
        orders, order_lines, order_totals, commissions, commissions_per_order
    WHERE
        orders.id = order_lines.order_id AND
        order_totals.order_id = orders.id  AND
        date(orders.created_at) = ? AND
        commissions.date = date(orders.created_at) AND
        commissions_per_order.date = date(orders.created_at)
"""


def get_report_for_date(date, db_name=DB_NAME):
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        row = cur.execute(SQL_SELECT_REPORT_FOR_DATE, (date,)).fetchone()
    except sqlite3.ProgrammingError:
        # ensure connection is closed even if an error occurs
        # TODO logging
        con.close()
        raise

    field_names = [description[0] for description in cur.description]
    results = [i for i in zip(field_names, row)]

    return results


@app.route('/<date>')
def report(date):
    try:
        # ensure the date param is a date string
        # in production this could be done by defining a schema
        # eg.: with Marshmallow, or using the OpenAPI spec and Swagger
        datetime.date.fromisoformat(date)
    except ValueError:
        # TODO logging
        return "Invalid date", 400

    try:
        results = get_report_for_date(date)
    except Exception:
        return "Server error", 500

    return json.dumps(dict(results)), 200, {'content-type': 'application/json'}


if __name__ == '__main__':
    app.run()
