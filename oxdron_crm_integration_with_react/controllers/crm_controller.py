import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

# Replace this with your actual API key
API_KEY = '8695d545367146260b18bdd91eae6b928c44566c'

class CRMController(http.Controller):
    
    @http.route('/api/crm/create', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def create_crm_record(self, **kwargs):
        # Check if the request is an OPTIONS preflight request
        if request.httprequest.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            return Response(status=200, headers=headers)

        # For the actual POST request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }

        # Validate API key
        request_api_key = request.httprequest.headers.get('Authorization')
        if request_api_key != f'Bearer {API_KEY}':
            _logger.error("Unauthorized access attempt")
            return Response(
                json.dumps({'success': False, 'error': 'Unauthorized'}),
                content_type='application/json',
                headers=headers,
                status=403
            )
        
        try:
            # Access JSON data from the request
            data = request.httprequest.get_json()
            _logger.info(f"Request Data: {data}")

            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            _logger.info(f"Received Data: name={name}, email={email}, phone={phone}")

            if not name or not email or not phone:
                _logger.error("Missing required fields")
                return Response(
                    json.dumps({'success': False, 'error': 'Missing required fields'}),
                    content_type='application/json',
                    headers=headers,
                    status=400
                )
            
            partner_id = request.env['res.partner'].sudo().search([('name', 'ilike', name), ('email', '=', email), ('phone', '=', phone)], limit=1)

            if not partner_id:
                # Create Contect Person
                partner_id = request.env['res.partner'].sudo().create({
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'mobile': phone
                })
                _logger.info(f"Contect Person Record Created: ID={partner_id.id}")

            # Create CRM lead
            crm_lead = request.env['crm.lead'].sudo().create({
                'name': name if name else '',
                'email_from': email if name else '',
                'phone': phone if name else '',
                'partner_id': partner_id.id if partner_id else ''
            })

            _logger.info(f"CRM Lead Record Created: ID={crm_lead.id}")

            return Response(
                json.dumps({'success': True, 'crm_lead_id': crm_lead.id}),
                content_type='application/json',
                headers=headers,
                status=200
            )
        except Exception as e:
            _logger.error(f"Error creating CRM record: {e}", exc_info=True)
            return Response(
                json.dumps({'success': False, 'error': str(e)}),
                content_type='application/json',
                headers=headers,
                status=500
            )
