import requests

class RequestHandler:
    def __init__(self, attack_type="dos"):
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
        if self.attack_type == "All":
            # simply send back the response
            return self.send_request(seed_input)
        elif self.attack_type == "dos":
            return self.dos_attack(seed_input)

    
    def dos_attack_success(self, response):
        # TODO decide how to dectect success
        if response.status_code == 200:
            return False
        else:
            return True