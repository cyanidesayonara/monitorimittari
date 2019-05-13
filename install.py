from shutil import copyfile
import subprocess


def main():
    subprocess.run(["pyinstaller", "-Fw", "main.py"])
    copyfile("default.json",
             "dist/default.json")
    copyfile("config.json",
             "dist/config.json")


if __name__ == "__main__":
    main()
