import subprocess
import config
import os
import re

def install_packages(pkg):
    command = ["sudo", "apt", "install", "-y"]
    command.extend(pkg)
    return command

def install_requirements():
    command = ["pip", "install", "-r", "requirements.txt"]
    return command

def packages():
    return config.packages

def main():
    subprocess.call(install_packages(packages()))
    install_requirements()
    subprocess.call(["python3", "setup.py"])

main()