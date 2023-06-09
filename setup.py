import subprocess
import config
import os
import re
import sh

def vscode_install():
    sh.sudo.snap("install", "--classic", "code")
    print("[debug]: installing vscode...")

def git_config():
    sh.git("config", "--global", "user.name", config.git_user)
    sh.git("config", "--global", "user.email", config.git_email)
    print("[debug]: Changing user configs...")

def start_agent():
    command = ["ssh-agent", "-s"]
    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    output.wait()

    ssh_stdout = output.stdout.readlines()
    ssh_stdout = "".join([i.decode() for i in ssh_stdout])

    SSH_AGENT_PID=re.search(r"SSH_AGENT_PID=([0-9]*)", ssh_stdout).group(1)
    SSH_AUTH_SOCK=re.search(r"SSH_AUTH_SOCK=(.*);[ ]", ssh_stdout).group(1)
    os.environ['SSH_AGENT_PID'] = SSH_AGENT_PID
    os.environ['SSH_AUTH_SOCK'] = SSH_AUTH_SOCK


def ssh_key_generate():
    start_agent()
    sh.ssh_add()
    try:
        sh.ssh_add()
    except:
        pass
    try:
        sh.ssh_add("-L")
        print("[debug]: Already generated ssh keys, skipping.")
    except:
        print("[debug]: Generating new ssh keys.")
        sh.ssh_keygen("-t", "ed25519", "-f", config.home_dir, "-q", "-N", "")
    sh.kill(['SSH_AGENT_PID'])
        sh.ssh_keygen("-t", "ed25519", "-f", config.home_dir + "/.ssh/id_ed25519", "-q", "-N", "")
    sh.kill(os.environ['SSH_AGENT_PID'])

#if this kill statement doesn't work, try modifying it. It doesn't like WSL

def main():
    ssh_key_generate()
    git_config()
    vscode_install()

main()

print("All done! :)")
input("press enter to continue.")
