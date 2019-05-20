from shutil import copyfile
import subprocess


def main():
    subprocess.run(["pyinstaller", "--onefile",
                    "--windowed", "--icon=eight.ico", "--clean", "main.py"])
    copyfile("config.json",
             "dist/config.json")


if __name__ == "__main__":
    main()
