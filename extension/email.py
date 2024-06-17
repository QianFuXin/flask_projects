# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     email.py
   Description :   
   Author :       FXQ
   date：          2024/6/17 17:20
-------------------------------------------------
"""
import yagmail


class FlaskQQEmail:
    def __init__(self, app=None):
        self._yag = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        qq_email = app.config.get("QQ_EMAIL", "")
        qq_email_password = app.config.get("QQ_EMAIL_PASSWORD", "")
        if not qq_email or not qq_email_password:
            raise ValueError("QQEmail or QQEmailPASSWORD is not set")
        self._yag = yagmail.SMTP(
            qq_email, qq_email_password, host="smtp.qq.com", port=465
        )

    @property
    def yag(self):
        return self._yag
