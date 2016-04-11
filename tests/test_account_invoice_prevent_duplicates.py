# This file is part of the account_invoice_prevent_duplicates module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_setup, doctest_teardown
from trytond.tests.test_tryton import doctest_checker


class AccountInvoicePreventDuplicatesTestCase(ModuleTestCase):
    'Test Account Invoice Prevent Duplicates module'
    module = 'account_invoice_prevent_duplicates'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoicePreventDuplicatesTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_invoice_prevent_duplicates.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
