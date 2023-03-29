import subprocess
import sh
import config


def install_packages(pkg):
    command = ["sudo", "apt", "install", "-y"]
    command.extend(pkg)
    return command


def packages():
    return config.packages


def vscode_install():
    sh.sudo.snap("install", "--classic", "code")
    print("[debug]: installing vscode...")


def git_config():
    sh.git("config", "--global", "user.name", config.git_user)
    sh.git("config", "--global", "user.email", config.git_email)
    print("[debug]: Changing user configs...")


def ssh_key_generate():
    if sh.ssh_add("-L") == "":
        sh.ssh_keygen("-t", "ed25519", "-f", config.home_dir)
    else:
        print("[debug]: Already generated ssh keys, skipping.")
        pass


subprocess.call(install_packages(packages()))
ssh_key_generate()
git_config()
vscode_install()

print("All done! :)")
input("press enter to continue.")
