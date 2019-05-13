from shutil import copyfile
import subprocess


def main():
    subprocess.run(["pyinstaller", "--onefile", "--windowed", "main.py"])
    copyfile("config.json",
             "dist/config.json")


if __name__ == "__main__":
    main()
