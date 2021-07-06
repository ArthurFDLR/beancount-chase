# Beancount Chase Bank Importer

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ArthurFDLR/beancount-chase/beancount-chase?style=for-the-badge)](https://github.com/ArthurFDLR/beancount-chase/actions)
[![PyPI](https://img.shields.io/pypi/v/beancount-chase?style=for-the-badge)](https://pypi.org/project/beancount-chase/)
[![PyPI - Version](https://img.shields.io/pypi/pyversions/beancount-chase.svg?style=for-the-badge)](https://pypi.org/project/beancount-chase/)
[![GitHub](https://img.shields.io/github/license/ArthurFDLR/beancount-chase?style=for-the-badge)](https://github.com/ArthurFDLR/beancount-chase/blob/master/LICENSE.txt)
[![Linting](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

`beancount-chase` is a [Beancount](http://furius.ca/beancount/) importer for [Chase Bank](https://www.chase.com/) CSV statements.

## Installation

```console
    $ pip install beancount-chase
```

## Usage

Add ```ChaseImporter``` to your [Beancount importers config file](https://beancount.github.io/docs/importing_external_data.html#configuration).
```python
from beancount_chase import ChaseBankImporter

CONFIG = [
    ChaseImporter(
        account='Assets:US:CB:Checking',
        expenseCat='Expenses:FIXME',    #Optional
        creditCat='Income:FIXME',       #Optional
    ),
]
```

## Contribution

Feel free to contribute!

Please make sure you have Python 3.6+ and [`Poetry`](https://poetry.eustace.io/) installed.

1. Git clone the repository - `git clone https://github.com/ArthurFDLR/beancount-chase`

2. Install the packages required for development - `poetry install`

3. That's basically it. You should now be able to run lint checks and the test suite - `make lint test`.
