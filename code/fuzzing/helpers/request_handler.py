import requests

class RequestHandler:
    def __init__(self, attack_type="login"):
        self.attack_type = attack_type
    
    def send_request(self, seed_input):
        seed_id = "&maine_seed_id=" + str(seed_input.id)
        if seed_input.method == "GET":
            response = requests.get(seed_input.url, params=seed_input.parameters + seed_id, headers=seed_input.headers)
        elif seed_input.method == "POST":
            response = requests.post(seed_input.url, data=seed_input.parameters + seed_id, headers=seed_input.headers)
        else:
            raise ValueError("Invalid method: {}".format(seed_input.method))

        return response
    
    def handle_request(self, seed_input):
        # TODO add more attack types
        response = self.send_request(seed_input)
        if self.attack_type == "All":
            # simply send back the response
            return response
        elif self.attack_type == "dos":
            return self.dos_attack_success(response)
        elif self.attack_type == "login":
            return self.login_attack_success(response)

    
    def dos_attack_success(self, response):
        # TODO decide how to dectect success
        if response.status_code == 200:
            return False
        else:
            return True
    
    def login_attack_success(self, response):
        # TODO decide how to dectect success
        if "Login successful" in response.text:
            return True
        else:
            return False