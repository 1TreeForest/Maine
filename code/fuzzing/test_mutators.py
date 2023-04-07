import unittest
from definition.seed_input import SeedInput
from helpers.mutators import StringMutator, ParameterMutator

class TestMutators(unittest.TestCase):

    def test_add_char(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = StringMutator.add_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) + 1)
        print("Mutation: add_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_delete_char(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = StringMutator.delete_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) - 1)
        print("Mutation: delete_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_char(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = StringMutator.replace_char(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_char")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_swap_chars(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = StringMutator.swap_chars(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: swap_chars")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_add_parameter(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = ParameterMutator.add_parameter(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: add_parameter")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_delete_parameter(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = ParameterMutator.delete_parameter(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        self.assertEqual(len(mutated_input.parameters), len(seed_input.parameters) - 14)
        print("Mutation: delete_parameter")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_key(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = ParameterMutator.replace_key(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_key")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

    def test_replace_value(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = ParameterMutator.replace_value(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: replace_value")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")
        
    def test_swap_paremeters(self):
        seed_input = SeedInput("https://example.com", 1, "GET", "param1=value1&param2=value2", {})
        mutated_input = ParameterMutator.swap_parameters(seed_input)
        self.assertNotEqual(mutated_input.parameters, seed_input.parameters)
        print("Mutation: swap_paremeters")
        print("Seed Input: ", seed_input)
        print("Mutated Input: ", mutated_input)
        print("-------------------------------")

if __name__ == '__main__':
    unittest.main()
