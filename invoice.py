#This file is part account_invoice_prevent_duplicates module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta

__all__ = ['Invoice']
__metaclass__ = PoolMeta

class Invoice:
    'Invoice'
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls._error_messages.update({
                'duplicate_invoice': ('The following supplier invoices have '
                    'duplicated information:\n\n%s'),
                'party_invoice_reference': ('Invoice: %(invoice)s\n'
                    'Party: %(party)s\nInvoice Reference: %(reference)s\n'),
                })

    @classmethod
    def write(cls, invoices, vals):
        super(Invoice, cls).write(invoices, vals)
        if vals.get('state') == 'open':
            pool = Pool()
            Translation = pool.get('ir.translation')
            for invoice in invoices:
                if not invoice.type in ('in_invoice','in_credit_note'):
                    continue
                domain = []
                domain.append(('party', '=', invoice.party.id))
                domain.append(('type', '=', invoice.type))
                domain.append(('invoice_date', '=', invoice.invoice_date))
                domain.append(('reference', '=', invoice.reference))
                domain.append(('state', 'in', ('open','done')))
                domain.append(('company', '=', invoice.company.id))
                invoices = cls.search(domain)
                if len(invoices) > 1:
                    language = Transaction().language
                    error = cls._error_messages['party_invoice_reference']
                    message = Translation.get_source('account.invoice',
                        'error', language, error)
                    if not message:
                        message = Translation.get_source(error, 'error',
                            language)
                    if message:
                        error = message
                    text = []
                    for invoice in cls.browse(invoices):
                        text.append(error % {
                                'invoice': invoice.rec_name or '',
                                'party': invoice.party.name,
                                'reference': invoice.reference,
                                })
                    text = '\n\n'.join( text )
                    cls.raise_user_error('duplicate_invoice', (text,))
