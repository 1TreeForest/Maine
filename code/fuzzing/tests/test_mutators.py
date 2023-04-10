import sys  
sys.path.append(r'code/fuzzing') 
import unittest
from definition.test_item import TestItem
from helpers.mutators import StringMutator, ParameterMutator

class TestMutators(unittest.TestCase):
    
    def test_add_char(self):
        string_mutator = StringMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = string_mutator.add_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) + 1)
        print("Mutation: add_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_delete_char(self):
        string_mutator = StringMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = string_mutator.delete_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) - 1)
        print("Mutation: delete_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_char(self):
        string_mutator = StringMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = string_mutator.replace_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_swap_chars(self):
        string_mutator = StringMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = string_mutator.swap_chars(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: swap_chars")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_add_parameter(self):
        parameter_mutator = ParameterMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = parameter_mutator.add_parameter(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: add_parameter")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_delete_parameter(self):
        parameter_mutator = ParameterMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = parameter_mutator.delete_parameter(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) - 14)
        print("Mutation: delete_parameter")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_key(self):
        parameter_mutator = ParameterMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = parameter_mutator.replace_key(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_key")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_value(self):
        parameter_mutator = ParameterMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = parameter_mutator.replace_value(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_value")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")
        
    def test_swap_paremeters(self):
        parameter_mutator = ParameterMutator()
        seed_input = TestItem("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = parameter_mutator.swap_parameters(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: swap_paremeters")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

if __name__ == '__main__':
    unittest.main()
