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
    def generate_random_string(length=10):
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
        new_params = seed_input.parameters
        if not new_params:
            return None
        del_key = random.choice(list(new_params.keys()))
        del new_params[del_key]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)
    
    @staticmethod
    def clear_parameter(seed_input, key):
        new_params = seed_input.parameters
        if key not in new_params:
            return None
        new_params[key] = ""
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_key(seed_input):
        new_params = seed_input.parameters
        if not new_params:
            return None
        old_key = random.choice(list(new_params.keys()))
        new_key = ParameterMutator.generate_random_string()
        new_params[new_key] = new_params.pop(old_key)
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_value(seed_input):
        new_params = seed_input.parameters
        if not new_params:
            return None
        key = random.choice(list(new_params.keys()))
        new_value = ParameterMutator.generate_random_string()
        new_params[key] = new_value
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)
    
    @staticmethod
    def swap_parameters(seed_input):
        new_params = seed_input.parameters
        if len(new_params) < 2:
            return None
        key_list = list(new_params.keys())
        random.shuffle(key_list)
        key1, key2 = key_list[:2]
        new_params[key1], new_params[key2] = new_params[key2], new_params[key1]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)
    
    @staticmethod
    def copy_value(seed_input):
        new_params = seed_input.parameters
        if not new_params:
            return None
        key1, key2 = random.sample(list(new_params.keys()), 2)
        new_params[key1] = new_params[key2]
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def copy_key(seed_input):
        new_params = seed_input.parameters
        if not new_params:
            return None
        key1, key2 = random.sample(list(new_params.keys()), 2)
        new_params[key1] = key2
        seed_input.increment_usage_count()
        return SeedInput(url=seed_input.url, parent_id=seed_input.id, method=seed_input.method, parameters=new_params, headers=seed_input.headers)