import os
import json
from defaults import defaults

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
                    self.left = data["left"]
                    self.right = data["right"]

    def getTheme(self):
        return self.theme

    def getResults(self):
        return self.left["results"] + self.right["results"]

    def getLeftResults(self):
        return self.left["results"]

    def getRightResults(self):
        return self.right["results"]

    def getInputFile(self):
        return self.inputFile
