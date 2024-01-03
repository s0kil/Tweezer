import argparse
import re
import tempfile
from pathlib import Path
from pprint import pprint

from Tweezer.GhidraBridge.ghidra_bridge import GhidraBridge
from Tweezer.Model.model import Model
from Tweezer.Training.trainer import Trainer


class Tweezer():
    def __init__(self, model_path="TweezerMDL"):
        self.model = None
        self.model_path = model_path

    def train(self, list_of_binary_folders):
        self.extend_model_training(list_of_binary_folders)

    def extend_model_training(self, list_of_binary_folders):
        trainer = Trainer()
        self.model = Model(self.model_path)
        with tempfile.TemporaryDirectory() as decom_output:
            trainer._generate_decompiled_functions_from_binaries(list_of_binary_folders, decom_output)

            for file_path in Path(decom_output).iterdir():
                binary_name, function_name, *epoc = Path(file_path).name.split("__")

                if "FUN" not in function_name:
                    print("Getting vectors for {}".format(file_path))
                    dataset = self.get_data_dict_from_file(file_path)
                    if "code" in dataset:
                        self.model.learn(dataset)
                    else:
                        print("Couldn't train off {}".format(file_path))

    def _sort_by_distance(self, dataset):
        """
        Sort the dataset by the 'distance' field from closest to farthest.

        :param dataset: A list of dictionaries, each with a 'distance' key.
        :return: The sorted dataset based on the 'distance' field.
        """
        return sorted(dataset, key=lambda x: x['distance'])

    def _get_code_from_decom_file(self, path_to_file):
        with open(path_to_file, "r") as file:
            code = file.read()
            pattern = re.compile(r'\{([^}]*)\}', re.DOTALL)
            match = pattern.search(code)

            if match.group(1).strip():
                return match.group(1).strip()
            else:
                return code

    def get_data_dict_from_file(self, file_path):
        function_dict = {}
        function_dict["binary_name"], function_dict["function_name"], *epoc = Path(file_path).name.split("__")
        function_dict["code"] = self._get_code_from_decom_file(file_path)
        return function_dict

    def find_closest_functions(self, function_file, number_of_closest=10):
        self.model = Model(self.model_path)

        function_dict = self.get_data_dict_from_file(function_file)

        if "code" not in function_dict:
            return "N/A"

        function_dict = self.model.process_code_and_append_vector(function_dict)

        if "vector" not in function_dict:
            return "N/A"

        dataset = self.model.find_closest_code(self.model.vectors, function_dict)

        return self._sort_by_distance(dataset)[:number_of_closest]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command-line interface Tweezer, binary analysis unknown function name finder.')

    # Model path argument (always required)
    parser.add_argument('--model-path', required=True, help='Path to the Tweezer model file')
    # Binary locations argument (accepts multiple values)
    parser.add_argument('--train', nargs='+', help='List of binary locations to train/extend training off')

    # Create a mutually exclusive group for --function and --binary
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--single-function', help='Path to a decompiled C file for analysis')
    group.add_argument('--binary', help='Path to binary to produce function name map from')

    args = parser.parse_args()

    return args


def entry():
    args = parse_args()

    # compare a decompiled function with vectors
    if args.single_function:

        if not Path(args.single_function).is_file():
            raise Exception("Provided function file '{}' is not a file or does not exist, please provide a valid "
                            "function file that contains a functions decompilation!")

        if not Path(args.model).is_file():
            raise Exception(
                "Model file at '{}' does not exist, please train a model first with the '--train' command or retrieve "
                "the example model from Github.")

        tweezer = Tweezer(args.model_path)
        print(tweezer.find_closest_functions(args.function))

    # Build a reference map of all functions in a binary
    elif args.binary:

        if not Path(args.binary).is_file():
            raise Exception("Provided binary '{}' is not a file or does not exist, please provide a valid binary that "
                            "is decompilable by Ghidra!")

        if not Path(args.model_path).is_file():
            raise Exception(
                "Model file at '{}' does not exist, please train a model first with the '--train' command or retrieve the example model from Github.")

        function_map = {}
        tweezer = Tweezer(args.model_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            g_bridge = GhidraBridge()
            g_bridge.decompile_binaries_functions(args.binary, tmpdirname)

            for file_path in Path(tmpdirname).iterdir():
                binary_name, function_name, *epoc = Path(file_path).name.split("__")

                closest_function = tweezer.find_closest_functions(file_path, 1)

                if isinstance(closest_function, list):
                    if len(closest_function) > 0:
                        if "function_name" in closest_function[0]:
                            closest_function_name = closest_function[0]["function_name"]
                            closest_function_binary = closest_function[0]["binary_name"]
                            function_map[function_name] = [closest_function_name, closest_function_binary]
                else:
                    print("Invalid closest function returned!")

        print("\n\n")
        print("=" * 20)
        pprint(function_map)
        print("=" * 20)
        print("\n\n")

    # Train / re train the model
    elif args.train:
        list_of_binary_folders = args.train
        tweezer = Tweezer(args.model_path)
        tweezer.train(list_of_binary_folders)


if __name__ == '__main__':
    entry()
