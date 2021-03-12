CREATE TABLE IF NOT EXISTS products (
  id PRIMARY KEY,
  description TEXT
);

CREATE TABLE IF NOT EXISTS promotions (
  id PRIMARY KEY,
  description TEXT
);

CREATE TABLE IF NOT EXISTS product_promotions (
  date DATE,
  product_id INTEGER REFERENCES products(id),
  promotion_id INTEGER REFERENCES promotions(id)
);

CREATE TABLE IF NOT EXISTS orders (
  id PRIMARY KEY,
  created_at DATETIME,
  vendor_id INTEGER,
  customer_id INTEGER
);

CREATE TABLE IF NOT EXISTS commissions (
  date DATE,
  vendor_id INTEGER,
  rate NUMERIC
);

CREATE TABLE IF NOT EXISTS order_lines (
  order_id INTEGER REFERENCES orders(id),
  product_id INTEGER REFERENCES products(id),
  product_description TEXT,
  product_price NUMERIC,
  product_vat_rate NUMERIC,
  discount_rate NUMERIC,
  quantity INTEGER,
  full_price_amount NUMERIC,
  discounted_amount NUMERIC,
  vat_amount NUMERIC,
  total_amount NUMERIC
)
