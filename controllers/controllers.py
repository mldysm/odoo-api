from odoo import http
from odoo.exceptions import ValidationError

class CustomNextjs(http.Controller):
    @http.route('/api', auth='public', website=False, csrf=False, type='json', methods=['GET', 'POST'])
    def index(self, **kw):
        partner_name = kw.get('partner_name')
        partner = http.request.env['res.partner'].sudo().search([('name', '=', partner_name)], limit=1)

        if not partner:
            partner = http.request.env['res.partner'].sudo().create({
                'name': partner_name,
                'phone': kw.get('partner_phone'),
                'email': kw.get('email_cc'),
            })

        http.request.env['helpdesk.ticket'].sudo().create({
            'name': kw.get('name', 'Default Ticket Name'),
            'partner_id': partner.id,
            'partner_phone': kw.get('partner_phone'),
            'email_cc': kw.get('email_cc'),
            'description': kw.get('description')
        })

        return kw
