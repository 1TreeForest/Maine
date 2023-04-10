import requests
import re

class RequestHandler:
    def __init__(self, vul_type="login"):
        self.vul_type = vul_type
    
    def send_request(self, seed_input, maine_test_id):
        if seed_input.parameters != "":
            maine_test_id = "maine_test_id=" + str(maine_test_id) + "&"
        else:
            maine_test_id = "maine_test_id=" + str(maine_test_id)
            
        if seed_input.method == "GET":
            response = requests.get(seed_input.url, params=maine_test_id + seed_input.parameters, headers=seed_input.headers)
        elif seed_input.method == "POST":
            response = requests.post(seed_input.url, data=maine_test_id + seed_input.parameters, headers=seed_input.headers)
        else:
            raise ValueError("Invalid method: {}".format(seed_input.method))
        
        # print(maine_test_id, response.url)
        return response
    
    def handle_request(self, seed_input, maine_test_id):
        # TODO add more attack types
        response = self.send_request(seed_input, maine_test_id)
        if self.vul_type == "All":
            # simply send back the response
            return response
        elif self.vul_type == "dos":
            return self.dos_vul_triggered(response)
        elif self.vul_type == "login":
            return self.login_vul_triggered(response)
        elif self.vul_type == "sqli":
            return self.sqli_vul_triggered(response)

    def dos_vul_triggered(self, response):
        # TODO decide how to dectect success
        if response.status_code == 200:
            return False
        else:
            return True
    
    def login_vul_triggered(self, response):
        # TODO decide how to dectect success
        if "login success" in response.text.lower():
            return True
        else:
            return False
        
    def sqli_vul_triggered(url, response):
        # 搜索响应内容是否存在常见的SQL错误消息
        pattern = re.compile(r"syntax error|mysql_fetch|mysql_num_rows|mysql_query|mysql_num_fields|mysql_fetch_array|mysql_result|mysql_list_tables|mysql_list_fields|mysql_numrows|mysql_numfields|You have an error in your SQL syntax|supplied argument is not a valid MySQL result resource|Column count doesn't match value count at row|Unknown column|mysql_fetch_assoc|mysql_fetch_row|mysql_insert_id|mysql_free_result|mysql_error|mysql_close|mysql_connect|mysql_select_db|mysql_num_rows|mysql_num_fields|mysql_db_query|mysql_list_dbs|mysql_list_tables|mysql_list_fields|mysql_fetch_object|mysql_affected_rows|mysql_create_db|mysql_drop_db|mysql_data_seek|mysql_field_seek|mysql_fetch_lengths|mysql_fetch_field|mysql_escape_string|mysql_real_escape_string|mysql_ping|mysql_stat|mysql_thread_id|mysql_character_set_name|mysql_set_charset|mysql_get_client_info|mysql_get_host_info|mysql_get_proto_info|mysql_get_server_info|mysql_info")
        if pattern.search(response.text):
            return True
        else:
            return False