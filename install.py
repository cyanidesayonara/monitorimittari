from shutil import copyfile
import subprocess


def main():
    subprocess.run(["pyinstaller",
                    "--onefile",
                    "--windowed",
                    "--add-data=icon.ico;.",
                    "--icon=icon.ico",
                    "--clean",
                    "--name=monitorimittari",
                    "main.py"]
                   )
    copyfile("config.json",
             "dist/config.json")


if __name__ == "__main__":
    main()
