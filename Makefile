migrate:
	sqlite3 ecomm.db < migrations/up.sql

loadfixtures:
	sqlite3 ecomm.db < fixtures.sql
