import sys  
sys.path.append(r'code/fuzzing')  
import random
import string
from definition.test_item import TestItem

class StringMutator:
    '''
    A class for mutating seed inputs' parameters by performing string-level operations.
    '''

    @staticmethod
    def add_char(seed_input):
        '''
        Add a random character to a random location in the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        try:
            pos = random.randint(0, len(new_params))
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        new_char = chr(random.randint(33, 126))
        new_params = new_params[:pos] + new_char + new_params[pos:]

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def delete_char(seed_input):
        '''
        Delete a random character from the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        try:
            pos = random.randint(0, len(new_params)-1)
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        new_params = new_params[:pos] + new_params[pos+1:]

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_char(seed_input):
        '''
        Replace a random character in the parameters string of a seed input with a random character.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        try:
            pos = random.randint(0, len(new_params)-1)
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        new_char = chr(random.randint(33, 126))
        new_params = new_params[:pos] + new_char + new_params[pos+1:]

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def swap_chars(seed_input):
        '''
        Swap two random characters in the parameters string of a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        new_params = seed_input.parameters
        try:
            pos1 = random.randint(0, len(new_params)-1)
            pos2 = random.randint(0, len(new_params)-1)
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        new_params = list(new_params)
        new_params[pos1], new_params[pos2] = new_params[pos2], new_params[pos1]
        new_params = ''.join(new_params)

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def random_mutate(seed_input):
        '''
        Randomly choose one of the string-level mutation methods to mutate a seed input.

        Args:
            seed_input (TestItem): The seed input to mutate.

        Returns:
            TestItem: The new seed input with mutated parameters.
        '''
        method = random.choice([StringMutator.add_char, StringMutator.delete_char, StringMutator.replace_char, StringMutator.swap_chars])

        return method(seed_input)

class ParameterMutator:
    @staticmethod
    def _generate_random_string(max_length=10):
        length = random.randint(0, max_length)
        return ''.join(random.choice(string.printable[33:126]) for _ in range(length))
    
    @staticmethod
    def add_parameter(seed_input):
        new_params = seed_input.parameters
        new_key = ParameterMutator._generate_random_string()
        new_value = ParameterMutator._generate_random_string()
        new_params += '&' + new_key + '=' + new_value

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def delete_parameter(seed_input):
        try:
            params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        key_to_delete = random.choice(list(params_dict.keys()))
        del params_dict[key_to_delete]
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_key(seed_input):
        try:
            params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        key_to_replace = random.choice(list(params_dict.keys()))
        new_key = ParameterMutator._generate_random_string()
        params_dict[new_key] = params_dict[key_to_replace]
        del params_dict[key_to_replace]
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def replace_value(seed_input):
        try:
            params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        key_to_replace_value = random.choice(list(params_dict.keys()))
        new_value = ParameterMutator._generate_random_string()
        params_dict[key_to_replace_value] = new_value
        new_params = '&'.join([f"{k}={v}" for k, v in params_dict.items()])

        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers)

    @staticmethod
    def swap_parameters(seed_input):
        try:
            params_dict = dict(param.split('=') for param in seed_input.parameters.split('&'))
            if len(params_dict) < 2:
                return seed_input
            idx1, idx2 = random.sample(range(len(params_dict)), 2)
            key1, value1 = params_dict[idx1].split("=")
            key2, value2 = params_dict[idx2].split("=")
            params_dict[idx1] = key1 + "=" + value2
            params_dict[idx2] = key2 + "=" + value1
            new_params = "&".join(params_dict)
        except:
            # 如果提取错误则证明不是和使用这种方法
            return seed_input
        
        return TestItem(url=seed_input.url, method=seed_input.method, parameters=new_params, headers=seed_input.headers) 
    
    @staticmethod
    def random_mutate(seed_input):
        method = random.choice([ParameterMutator.add_parameter, ParameterMutator.delete_parameter, ParameterMutator.replace_key, ParameterMutator.replace_value, ParameterMutator.swap_parameters])

        return method(seed_input)