__version__ = '0.1.0'

from beancount.core.number import D
from beancount.ingest import importer
from beancount.core import data, flags
from beancount.core.amount import Amount
from beancount.core.number import Decimal

from datetime import datetime
import csv


class ChaseBankImporter(importer.ImporterProtocol):
    """ Beancount Importer for Chase Bank CSV statements.

    Attributes:
        account (str): Account name in beancount format (e.g. 'Assets:FR:CdE:CompteCourant')
        expenseCat (str, optional): Expense category in beancount format (e.g. 'Expenses:FIXME'). Defaults to '', no expense posting added to the operation.
        creditCat (str, optional): Income category in beancount format (e.g. 'Income:FIXME'). Defaults to '', no income posting added to the operation.
    """
    def __init__(
        self,
        account: str,
        expenseCat: str = '',
        creditCat: str = '',
        file_encoding: str = 'utf-8',
    ):
        self.account = account
        self.expenseCat = expenseCat
        self.creditCat = creditCat
        self.file_encoding = file_encoding

    def name(self):
        return 'Chase Bank: {}'.format(self.__class__.__name__)

    def file_account(self, _):
        return self.account

    def file_name(self, _):
        return 'Chase_Statement.csv'

    def file_date(self, file_):

        if not self.identify(file_):
            return None

        date = None

        with open(file_.name, encoding=self.file_encoding) as fd:
            reader = csv.DictReader(
                fd, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"'
            )

            for line in reader:
                date_tmp = datetime.strptime(
                    line['Posting Date'], '%m/%d/%Y'
                ).date()
                if not date or date_tmp > date:
                    date = date_tmp

        return date

    def extract(self, file_, existing_entries=None):
        entries = []

        if not self.identify(file_):
            return []

        n = file_ if type(file_) == str else file_.name

        with open(n, encoding=self.file_encoding) as fd:
            reader = csv.DictReader(
                fd, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"'
            )

            for index, line in enumerate(reader):
                meta = data.new_metadata(n, index)

                payee = line['Description']
                currency = 'USD'
                amount = Decimal(line['Amount'])
                isExpense = line['Details'] == 'DEBIT'

                postings = [
                    data.Posting(
                        self.account,
                        Amount(amount, currency),
                        None,
                        None,
                        None,
                        None,
                    )
                ]

                if isExpense and len(self.expenseCat) > 0:
                    postings.append(
                        data.Posting(
                            self.expenseCat,
                            Amount(-amount, currency),
                            None,
                            None,
                            None,
                            None,
                        )
                    )
                if not isExpense and len(self.creditCat) > 0:
                    postings.append(
                        data.Posting(
                            self.creditCat,
                            Amount(
                                (amount if isExpense else -amount), currency
                            ),
                            None,
                            None,
                            None,
                            None,
                        )
                    )

                entries.append(
                    data.Transaction(
                        meta=meta,
                        date=datetime.strptime(
                            line['Posting Date'], '%m/%d/%Y'
                        ).date(),
                        flag=flags.FLAG_OKAY,
                        payee=payee,
                        narration=line['Type'],
                        tags=data.EMPTY_SET,
                        links=data.EMPTY_SET,
                        postings=postings,
                    )
                )
        return entries

    def is_valid_header(self, line: str) -> bool:
        expected_values = [
            'Details',
            'Posting Date',
            'Description',
            'Amount',
            'Type',
            'Balance',
            'Check or Slip #',
        ]
        actual_values = [column.strip('"') for column in line.split(',')]
        if len(expected_values) != len(actual_values):
            return False
        for (expected, actual) in zip(expected_values, actual_values):
            if expected != actual:
                return False
        return True

    def identify(self, file_) -> bool:
        n = file_ if type(file_) == str else file_.name

        with open(n, encoding=self.file_encoding) as fd:
            try:
                line = fd.readline().strip()
            except:
                return False
        return self.is_valid_header(line)
