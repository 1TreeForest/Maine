import random
import string
from definition.seed_input import SeedInput

class StringMutator:
    '''
    A class for mutating seed inputs' parameters by performing string-level operations.
    '''

    @staticmethod
    def add_char(seed_input):
        '''
        Add a random character to a random location in the parameters string of a seed input.

        Args:
            seed_input (SeedInput): The seed input to mutate.

        Returns:
            SeedInput: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        pos = random.randint(0, len(new_params))
        new_char = chr(random.randint(33, 126))
        new_params = new_params[:pos] + new_char + new_params[pos:]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def delete_char(seed_input):
        '''
        Delete a random character from the parameters string of a seed input.

        Args:
            seed_input (SeedInput): The seed input to mutate.

        Returns:
            SeedInput: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        pos = random.randint(0, len(new_params)-1)
        new_params = new_params[:pos] + new_params[pos+1:]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_char(seed_input):
        '''
        Replace a random character in the parameters string of a seed input with a random character.

        Args:
            seed_input (SeedInput): The seed input to mutate.

        Returns:
            SeedInput: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        pos = random.randint(0, len(new_params)-1)
        new_char = chr(random.randint(33, 126))
        new_params = new_params[:pos] + new_char + new_params[pos+1:]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def swap_chars(seed_input):
        '''
        Swap two random characters in the parameters string of a seed input.

        Args:
            seed_input (SeedInput): The seed input to mutate.

        Returns:
            SeedInput: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        pos1 = random.randint(0, len(new_params)-1)
        pos2 = random.randint(0, len(new_params)-1)
        new_params = list(new_params)
        new_params[pos1], new_params[pos2] = new_params[pos2], new_params[pos1]
        new_params = ''.join(new_params)
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)


class ParameterMutator:
    @staticmethod
    def generate_random_string(max_length=10):
        length = random.randint(0, max_length)
        return ''.join(random.choice(string.printable[33:127]) for _ in range(length))
    
    @staticmethod
    def add_parameter(seed_input):
        new_params = seed_input.parameters
        new_key = ParameterMutator.generate_random_string()
        new_value = ParameterMutator.generate_random_string()
        new_params += '&' + new_key + '=' + new_value
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def delete_parameter(seed_input):
        params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        if not params_dict:  # 检查参数是否为空
            return seed_input
        key_to_delete = random.choice(list(params_dict.keys()))
        del params_dict[key_to_delete]
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_key(seed_input):
        params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        if not params_dict:  # 检查参数是否为空
            return seed_input
        key_to_replace = random.choice(list(params_dict.keys()))
        new_key = ParameterMutator.generate_random_string()
        params_dict[new_key] = params_dict[key_to_replace]
        del params_dict[key_to_replace]
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_value(seed_input):
        params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        if not params_dict:  # 检查参数是否为空
            return seed_input
        key_to_replace_value = random.choice(list(params_dict.keys()))
        new_value = ParameterMutator.generate_random_string()
        params_dict[key_to_replace_value] = new_value
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def swap_parameters(seed_input):
        params = seed_input.parameters.split("&")
        if len(params) < 2:
            return seed_input
        idx1, idx2 = random.sample(range(len(params)), 2)
        key1, value1 = params[idx1].split("=")
        key2, value2 = params[idx2].split("=")
        params[idx1] = key1 + "=" + value2
        params[idx2] = key2 + "=" + value1
        new_params = "&".join(params)
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)