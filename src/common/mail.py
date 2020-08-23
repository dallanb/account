import os
from flask import render_template


class Mail:
    def __init__(self):
        pass

    def generate_body(self, template, **kwargs):
        return render_template(
            self.get_filename(template),
            **kwargs
        )

    @staticmethod
    def get_filename(template):
        return os.path.join('email', f'{template}.html')
