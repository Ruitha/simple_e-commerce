import requests # type: ignore

class IntaSend:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def create_payment(self, amount, currency, customer_email):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'amount': amount,
            'currency': currency,
            'customer_email': customer_email
        }
        response = requests.post('https://api.intasend.com/v1/payments', headers=headers, json=data)
       