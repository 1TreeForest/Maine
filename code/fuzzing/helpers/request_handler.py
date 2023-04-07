import requests

class RequestHandler:
    def handle_request(self, seed_input):
        seed_id = "&seed_id=" + str(seed_input.id)
        if seed_input.method == "GET":
            response = requests.get(seed_input.url, params=seed_input.parameters + seed_id, headers=seed_input.headers)
        elif seed_input.method == "POST":
            response = requests.post(seed_input.url, data=seed_input.parameters + seed_id, headers=seed_input.headers)
        else:
            raise ValueError("Invalid method: {}".format(seed_input.method))

        return response
