from django.core.exceptions import ValidationError
import re

class ValidatePasswordHasLetterAndDigit:
    def validate(self, password, user=None):
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValidationError(
                'Password must contain at least one letter and one digit.',
                code='password_no_letter_digit'
            )

    def get_help_text(self):
        return 'Your password must contain at least one letter and one digit.'