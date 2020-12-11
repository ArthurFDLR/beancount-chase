import pathlib
import pytest
import datetime

from beancount_chase import __version__, ChaseBankImporter
from beancount.core.number import Decimal

TEST_FILE_NAME = 'test_file.csv'

TEST_DATE = datetime.date(2020, 12, 1)


def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def filename():
    return pathlib.Path(__file__).parent.absolute() / TEST_FILE_NAME


@pytest.fixture
def importer():
    return ChaseBankImporter('Assets:CB')


def test_identify(importer, filename):
    with open(filename) as fd:
        assert importer.identify(fd)


def test_file_date(importer, filename):
    with open(filename) as fd:
        assert importer.file_date(fd) == TEST_DATE


def test_extract(importer, filename):
    with open(filename) as fd:
        operations = importer.extract(fd)

    operations_test = [
        {
            'date': datetime.date(2020, 12, 1),
            'amount': Decimal('-59.17'),
            'payee': 'Desc Debit 2             11/30',
        },
        {
            'date': datetime.date(2020, 10, 13),
            'amount': Decimal('100.00'),
            'payee': 'Desc Credit 2',
        },
        {
            'date': datetime.date(2020, 10, 5),
            'amount': Decimal('-11.78'),
            'payee': 'Desc Debit 1           10/04',
        },
        {
            'date': datetime.date(2020, 10, 5),
            'amount': Decimal('465.53'),
            'payee': 'Desc Credit 1    1465436878       WEB ID: 453233521',
        },
    ]
    op_name_test = [op_test['payee'] for op_test in operations_test]

    assert len(operations) == len(operations_test)

    for op in operations:

        assert op.payee in op_name_test, 'Missing operation'
        op_test = operations_test[op_name_test.index(op.payee)]

        assert op.payee == op_test['payee'], 'Wrong payee name'
        assert op.date == op_test['date'], 'Wrong date'

        assert len(op.postings) == 1
        assert op.postings[0].account == 'Assets:CB', 'Wrong account name'
        assert op.postings[0].units.currency == 'USD', 'Wrong currency'
        assert op.postings[0].units.number == op_test['amount'], 'Wrong amount'
