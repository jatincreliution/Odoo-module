# -*- coding: utf-8 -*-

import logging
from itertools import chain
from odoo.http import request
from odoo import api, models

_logger = logging.getLogger(__name__)
USER_PRIVATE_FIELDS = ['password']
concat = chain.from_iterable


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _check_credentials(self, password, user_agent_env):
        """ Check user credentials during login and log the login details."""
        result = super(ResUsers, self)._check_credentials(
            password, user_agent_env)
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        vals = {
            'name': self.name,
            'ip_address': ip_address
        }
        self.env['login.detail'].sudo().create(vals)
        return result
