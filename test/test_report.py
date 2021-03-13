from unittest.mock import patch
import sqlite3

import pytest

from app import report, SQL_SELECT_REPORT_FOR_DATE, DB_NAME


class TestReport:
    @pytest.mark.parametrize(
        'date', [
            '2019-00-00',
            '0000-00-00',
            'invalid date here',
        ]
    )
    def test_invalid_date(self, date):
        assert report(date) == ('Invalid date', 400)

    @pytest.mark.parametrize(
        'date', [
            '2019-01-01',
            '1982-11-14',
        ]
    )
    @patch('app.get_report_for_date')
    def test_valid_date(self, mock_report, date):
        mock_report.return_value = []

        assert report(date) == (
            '{}', 200, {'content-type': 'application/json'}
        )

    def test_sql_query_smoke_test(self):
        '''
        Run the SQL statement on an empty DB just to ensure
        there are no syntax errors
        '''
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        date = '2021-03-12'

        cur.execute(SQL_SELECT_REPORT_FOR_DATE, (date,)).fetchone()
