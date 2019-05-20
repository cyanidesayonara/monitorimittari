import os
import json
from defaults import defaults
from result import Result

configFile = "config.json"


class Repository:
    def __init__(self):
        if not os.path.isfile(configFile):
            with open(configFile, "w+") as f:
                f.write(json.dumps(defaults))

        # open and load config
        with open(configFile) as f:

            data = json.loads(f.read())
            self.theme = data["theme"]
            self.inputFile = data["inputFile"]
            self.outputFile = data["outputFile"]
            self.inputFile = data["inputFile"]

            leftLNumber = data["left"]["lnumber"]
            self.leftLNumber = Result(
                name=leftLNumber["name"],
                value=leftLNumber["value"],
                cell=leftLNumber["cell"]
            )

            rightLNumber = data["right"]["lnumber"]
            self.rightLNumber = Result(
                name=rightLNumber["name"],
                value=rightLNumber["value"],
                cell=rightLNumber["cell"]
            )

            leftTester = data["left"]["tester"]
            self.leftTester = Result(
                name=leftTester["name"],
                value=leftTester["value"],
                cell=leftTester["cell"]
            )

            rightTester = data["right"]["tester"]
            self.rightTester = Result(
                name=rightTester["name"],
                value=rightTester["value"],
                cell=rightTester["cell"]
            )

            self.leftResults = []
            for result in list(data["left"]["results"]):
                result = Result(
                    name=result["name"],
                    value=result["value"],
                    cell=result["cell"],
                )
                self.leftResults.append(result)

            self.rightResults = []
            for result in list(data["right"]["results"]):
                result = Result(
                    name=result["name"],
                    value=result["value"],
                    cell=result["cell"],
                )
                self.rightResults.append(result)

            self.results = self.leftResults + self.rightResults

    def freeze(self):
        configFile = "config.json"

        data = {
            "theme": self.theme,
            "inputFile": self.inputFile,
            "outputFile": self.outputFile,
            "left": {
                "lnumber": self.leftLNumber.__dict__,
                "tester": self.leftTester.__dict__,
                "results": [result.__dict__ for result in self.leftResults],
            },
            "right": {
                "lnumber": self.rightLNumber.__dict__,
                "tester": self.rightTester.__dict__,
                "results": [result.__dict__ for result in self.rightResults],
            }
        }

        with open(configFile, "w+") as f:
            f.write(json.dumps(data))
