# This file is part account_invoice_prevent_duplicates module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool
from trytond.i18n import gettext
from trytond.exceptions import UserError


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        # Reference should be required to detect duplicates
        if 'type' not in cls.reference.depends:
            old_required = cls.reference.states.get('required', Bool(False))
            cls.reference.states.update({
                    'required': old_required | ((Eval('type') == 'in')
                        & ~Eval('state').in_(['draft', 'cancelled']))
                    })
            cls.reference.depends.append('type')

    @property
    def duplicate_invoice_domain(self):
        domain = []
        domain.append(('party', '=', self.party.id))
        domain.append(('type', '=', self.type))
        domain.append(('invoice_date', '=', self.invoice_date))
        domain.append(('reference', '=', self.reference))
        domain.append(('state', 'in', ('posted', 'paid')))
        domain.append(('company', '=', self.company.id))
        domain.append(('id', '!=', self.id))
        return domain

    @classmethod
    def set_number(cls, invoices):
        language = Transaction().language

        super().set_number(invoices)

        for invoice in invoices:
            if invoice.type != 'in':
                continue
            duplicated_invoices = cls.search(
                invoice.duplicate_invoice_domain, limit=1)
            if duplicated_invoices:
                message = gettext(
                    'account_invoice_prevent_duplicates.party_invoice_reference',
                    language=language)
                if message:
                    error = message
                text = []
                for invoice in [invoice] + duplicated_invoices:
                    text.append(error % {
                            'invoice': invoice.rec_name or '',
                            'party': invoice.party.name,
                            'reference': invoice.reference,
                            })
                text = '\n\n'.join(text)
                raise UserError(gettext(
                    'account_invoice_prevent_duplicates.duplicate_invoice',
                        message=text))
