import sys  
sys.path.append(r'code/fuzzing')  
import random
from definition.test_item import TestItem
import re

class StringMutator:
    '''
    A class for mutating seed inputs' parameters by performing string-level operations.
    '''

    def _generate_random_char(self):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        specials = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        if random.random() < 0.2:
            return random.choice(characters)
        else:
            return random.choice(specials)

    def add_char(self, seed_input):
        '''
        Add a random character to a random location in the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        new_char = self._generate_random_char()
        if len(new_params) != 0:
            pos = random.randint(0, len(new_params))
            new_params = new_params[:pos] + new_char + new_params[pos:]
        else:
            new_params = new_char
        
        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def delete_char(self, seed_input):
        '''
        Delete a random character from the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        if len(new_params) == 0:
            return None
        pos = random.randint(0, len(new_params)-1)
        new_params = new_params[:pos] + new_params[pos+1:]

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def replace_char(self, seed_input):
        '''
        Replace a random character in the parameters string of a seed input with a random character.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        if len(new_params) == 0:
            return None
        pos = random.randint(0, len(new_params)-1)
        new_char = self._generate_random_char()
        new_params = new_params[:pos] + new_char + new_params[pos+1:]

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def swap_chars(self, seed_input):
        '''
        Swap two random characters in the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        if len(new_params) < 2:
            return None
        pos1 = random.randint(0, len(new_params)-1)
        pos2 = random.randint(0, len(new_params)-1)
        new_params = list(new_params)
        new_params[pos1], new_params[pos2] = new_params[pos2], new_params[pos1]
        new_params = ''.join(new_params)

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def random_mutate(self, seed_input, vul_type="All"):
        '''
        Randomly choose one of the string-level mutation methods to mutate a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        method = random.choice([
            self.add_char,
            self.delete_char,
            self.replace_char,
            self.swap_chars
        ])

        return method(seed_input)

class ParameterMutator:
    def __init__(self, vul_type="All"):
        with open('code/fuzzing/dicts/dict_%s.txt' % vul_type, 'r') as f:
            self.dict = f.readlines()

    def _generate_random_string(self, max_length=10):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?"
        length = random.randint(0, max_length)
        return ''.join(random.choice(characters) for _ in range(length))

    def _generate_string_from_dict_file(self, max_length=10):
        pass

    def add_parameter(self, seed_input):
        new_params = seed_input.parameters
        if new_params != "":
            new_params += '&'
        new_key = self._generate_random_string()
        new_value = self._generate_random_string()
        
        new_params += new_key + '=' + new_value

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def delete_parameter(self, seed_input):
        pattern = re.compile(r'(?:(?<=^)|(?<=&))([^&=]+)=([^&]+)')
        params_list = re.findall(pattern, seed_input.parameters)
        if not params_list:
            return None
        key_to_delete = random.choice(list(range(len(params_list))))
        del params_list[key_to_delete]
        new_params = '&'.join([f"{k}={v}" for k, v in params_list])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def replace_key(self, seed_input):
        pattern = re.compile(r'(?:(?<=^)|(?<=&))([^&=]+)=([^&]+)')
        params_list = re.findall(pattern, seed_input.parameters)
        if not params_list:
            return None
        key_to_replace = random.choice(list(range(len(params_list))))
        new_key = self._generate_random_string()
        params_list[key_to_replace] = (new_key, params_list[key_to_replace][1])
        new_params = '&'.join([f"{k}={v}" for k, v in params_list])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def replace_value(self, seed_input):
        pattern = re.compile(r'(?:(?<=^)|(?<=&))([^&=]+)=([^&]+)')
        params_list = re.findall(pattern, seed_input.parameters)
        if not params_list:
            return None
        key_to_replace_value = random.choice(list(range(len(params_list))))
        new_value = self._generate_random_string()
        params_list[key_to_replace_value] = (params_list[key_to_replace_value][0], new_value)
        new_params = '&'.join([f"{k}={v}" for k, v in params_list])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    def swap_parameters(self, seed_input):
        pattern = re.compile(r'(?:(?<=^)|(?<=&))([^&=]+)=([^&]+)')
        params_list = re.findall(pattern, seed_input.parameters)
        if len(params_list) < 2:
            return None
        idx1, idx2 = random.sample(range(len(params_list)), 2)
        _, value1 = params_list[idx1]
        _, value2 = params_list[idx2]
        params_list[idx1] = (params_list[idx1][0], value2)
        params_list[idx2] = (params_list[idx2][0], value1)
        new_params = "&".join([f"{k}={v}" for k, v in params_list])
        
        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)
        
    def random_mutate(self, seed_input, vul_type="All"):
        method = random.choice([
            self.add_parameter,
            self.delete_parameter,
            self.replace_key,
            self.replace_value,
            self.swap_parameters])
        
        return method(seed_input)