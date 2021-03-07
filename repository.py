import os
import json
from defaults import defaults
from result import Result

CONFIG_FILE = "config.json"


class Repository:
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, "w+") as file:
                file.write(json.dumps(defaults, indent=2))

        # open and load config
        with open(CONFIG_FILE) as file:
            data = json.loads(file.read())
            self.theme = data["theme"]
            self.input_file = data["inputFile"]
            self.output_file = ""

            left_l_number = data["left"]["lnumber"]
            self.left_l_number = Result(
                name=left_l_number["name"],
                value=left_l_number["value"],
                cell=left_l_number["cell"]
            )

            right_l_number = data["right"]["lnumber"]
            self.right_l_number = Result(
                name=right_l_number["name"],
                value=right_l_number["value"],
                cell=right_l_number["cell"]
            )

            left_tester = data["left"]["tester"]
            self.left_tester = Result(
                name=left_tester["name"],
                value=left_tester["value"],
                cell=left_tester["cell"]
            )

            right_tester = data["right"]["tester"]
            self.right_tester = Result(
                name=right_tester["name"],
                value=right_tester["value"],
                cell=right_tester["cell"]
            )

            self.left_results = []
            for result in list(data["left"]["results"]):
                result = Result(
                    name=result["name"],
                    value=result["value"],
                    cell=result["cell"],
                )
                self.left_results.append(result)

            self.right_results = []
            for result in list(data["right"]["results"]):
                result = Result(
                    name=result["name"],
                    value=result["value"],
                    cell=result["cell"],
                )
                self.right_results.append(result)

            self.results = self.left_results + self.right_results

    def freeze(self):
        data = {
            "theme": self.theme,
            "inputFile": self.input_file,
            "left": {
                "lnumber": self.left_l_number.__dict__,
                "tester": self.left_tester.__dict__,
                "results": [result.__dict__ for result in self.left_results],
            },
            "right": {
                "lnumber": self.right_l_number.__dict__,
                "tester": self.right_tester.__dict__,
                "results": [result.__dict__ for result in self.right_results],
            }
        }

        with open(CONFIG_FILE, "w+") as file:
            file.write(json.dumps(data, indent=2))
