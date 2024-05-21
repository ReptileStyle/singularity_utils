import socket
import subprocess

def block_ip(ip):
    """
    Block incoming and outgoing traffic for the specified IP address.
    Uses netsh on Windows. Make sure to adjust or run with appropriate permissions.
    """
    # Block incoming traffic
    try:
        subprocess.check_call(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="Block Incoming ' + ip + '"', 'dir=in', 'action=block', 'remoteip=' + ip])
        print(f"Blocked incoming traffic for IP {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block incoming traffic for IP {ip}: {e}")

    # Block outgoing traffic
    try:
        subprocess.check_call(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="Block Outgoing ' + ip + '"', 'dir=out', 'action=block', 'remoteip=' + ip])
        print(f"Blocked outgoing traffic for IP {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block outgoing traffic for IP {ip}: {e}")

def main():
    domain = "account.jetbrains.com"
    try:
        ips = socket.gethostbyname_ex(domain)[2]
        for ip in ips:
            print(f"Blocking IP: {ip}")
            block_ip(ip)
    except socket.gaierror as e:
        print(f"Failed to lookup IP addresses for {domain}: {e}")

if __name__ == "__main__":
    main() 
