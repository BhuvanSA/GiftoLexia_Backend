import re


class ResponseValidator:
    def __init__(self, response):
        self.response = response

    def validate_email(self):
        email = self.response.get('email')
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        return False

    def validate_name(self):
        name = self.response.get('name').strip()
        if name != '':
            return True
        return False

    def validate_language(self):
        allowed_languages = [
            "English", "Hindi", "Kannada", "Marathi",
            "Malayalam", "Tamil", "Telugu", "Punjabi"
        ]
        language = self.response.get('language')
        if language in allowed_languages:
            return True
        return False

    def validate_age(self):
        allowed_ages = [
            "3-5", "5-8", "8-12",
        ]
        age = self.response.get('age')
        if age in allowed_ages:
            return True
        return False

    def validate(self):
        email_valid = self.validate_email()
        name_valid = self.validate_name()
        language_valid = self.validate_language()
        age_valid = self.validate_age()
        # print(email_valid, name_valid, language_valid, age_valid)
        return email_valid and name_valid and language_valid and age_valid


if __name__ == '__main__':
    # Test the validator
    response_data = {
        'email': 'bhuvan.s.a.raj.2003@gmail.com',
        'name': 'ILoveProgramming',
        'language': 'Hindi',
        'age': '3-5'
    }

    validator = ResponseValidator(response_data)
    is_valid = validator.validate()

    if is_valid:
        print("Response is valid.")
    else:
        print("Response is not valid.")
