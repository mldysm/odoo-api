from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class CustomNextjs(http.Controller):
    @http.route('/ticket/create', auth='public', website=False, csrf=False, type='json', methods=['GET', 'POST', 'OPTIONS'], cors='*')
    def index(self, **kw):
        if request.httprequest.method == 'POST':
            _logger.info('aku adalah post')
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, PUT',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
            # return request.make_response('', headers=headers)

            partner_name = kw.get('partner_name')
            partner_phone = kw.get('partner_phone')
            email_cc = kw.get('email_cc')

        # Validate the data
            if not partner_name or not partner_phone or not email_cc:
                raise ValidationError("Missing required fields")

            partner = http.request.env['res.partner'].sudo().search([('name', '=', partner_name)], limit=1)

            if not partner:
                partner = http.request.env['res.partner'].sudo().create({
                    'name': partner_name,
                    'phone': partner_phone,
                    'email': email_cc,
                })

            ticket = http.request.env['helpdesk.ticket'].sudo().create({
                'name': kw.get('name', 'Default Ticket Name'),
                'partner_id': partner.id,
                'partner_phone': partner_phone,
                'email_cc': email_cc,
                'description': kw.get('description')
            })

            # return kw
            return request.make_response(kw, headers=headers)

class NewTickets(http.Controller):

    @http.route(["/my/tickets/new"], type="http", auth="user", method=["POST", "GET"], website=True)
    def createNewTicket(self, **kw):
        ticket_list = request.env['helpdesk.ticket'].search([])
        if request.httprequest.method == "POST":
            _logger.info(kw)

            partner_name = kw.get('partner_name')
            partner_phone = kw.get('partner_phone')
            email_cc = kw.get('email_cc')

            if not partner_name or not partner_phone or not email_cc:
                raise ValidationError("Missing required fields")

            partner = http.request.env['res.partner'].sudo().search([('name', '=', partner_name)], limit=1)

            if not partner:
                partner = http.request.env['res.partner'].sudo().create({
                    'name': partner_name,
                    'phone': partner_phone,
                    'email': email_cc,
                })

            ticket = http.request.env['helpdesk.ticket'].sudo().create({
                'name': kw.get('name', 'Default Ticket Name'),
                'partner_id': partner.id,
                'partner_phone': partner_phone,
                'email_cc': email_cc,
                'description': kw.get('description')
            })
        else:
            _logger.info("GET METHOD..........................")
        return request.render("custom_nextjs.new_ticket_form_view_portal", {'tickets':ticket_list, 'page_name':"create_tickets"})

