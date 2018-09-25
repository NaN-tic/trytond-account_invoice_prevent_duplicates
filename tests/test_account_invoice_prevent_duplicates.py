# This file is part of the account_invoice_prevent_duplicates module for Tryton
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class AccountInvoicePreventDuplicatesTestCase(ModuleTestCase):
    'Test Account Invoice Prevent Duplicates module'
    module = 'account_invoice_prevent_duplicates'

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoicePreventDuplicatesTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_invoice_prevent_duplicates.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
