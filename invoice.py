#This file is part account_invoice_prevent_duplicates module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import Workflow, ModelView, ModelSQL
from trytond.transaction import Transaction
from trytond.pool import Pool


class Invoice(Workflow, ModelSQL, ModelView):
    _name = 'account.invoice'

    def __init__(self):
        super(Invoice, self).__init__()
        self._error_messages.update({
                'duplicate_invoice': 'The following supplier invoices have '
                    'duplicated information:\n\n%s',
                'party_invoice_reference': 'Invoice Number: %(number)s\n'\
                    'Party: %(party)s\nInvoice Reference: %(reference)s\n\n'
                })

    def write(self, ids, vals):
        res = super(Invoice, self).write(ids, vals)
        if vals.get('state') == 'open':
            pool = Pool()
            translation_obj = pool.get('ir.translation')
            for invoice in self.browse(ids):
                if not invoice.type in ('in_invoice','in_credit_note'):
                    continue
                domain = []
                domain.append(('party', '=', invoice.party.id))
                domain.append(('type', '=', invoice.type))
                domain.append(('invoice_date', '=', invoice.invoice_date))
                domain.append(('reference', '=', invoice.reference))
                domain.append(('state', 'in', ('open','done')))
                invoice_ids = self.search(domain)
                if len(invoice_ids) > 1:
                    language = Transaction().language
                    error = self._error_messages['party_invoice_reference']
                    message = translation_obj.get_source('account.invoice', 
                        'error', language, error)
                    if not message:
                        message = translation_obj.get_source(error, 'error', language)
                    if message:
                        error = message
                    text = []
                    for invoice in self.browse(invoice_ids):
                        text.append(error % {
                                'number': invoice.number or '',
                                'party': invoice.party.name, 
                                'reference': invoice.reference,
                                })
                    text = '\n\n'.join( text )
                    self.raise_user_error('duplicate_invoice', (text,))
        return res

Invoice()
