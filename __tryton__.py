#This file is part account_invoice_prevent_duplicates module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Account Invoice Prevent Duplicates',
    'version': '2.3.0',
    'author': 'NaN·tic',
    'email': 'info@NaN-tic.com',
    'website': 'http://www.tryton.org/',
    'description': 'Prevents duplicate supplier invoices by checking no other'\
        'invoice has the same party, date and reference when the user '\
        'tries to open an invoice.',
    'depends': [
        'ir',
        'account',
        'company',
        'party',
        'product',
        'res',
        'currency',
        'account_product',
        'account_invoice',
        ],
    'xml': [
        ],
    'translation': [
        'locale/ca_ES.po',
        ]
}
