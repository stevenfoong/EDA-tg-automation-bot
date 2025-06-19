#from utils.bash_runner import run_bash_command

async def ping_host(host):
    cmd = f"ping -c 4 {host}"
#    await run_bash_command(cmd)

async def lookup_ip_location(ip=None):
    """
    Use curl to query the IP location.
    If no IP is provided, query the container's public IP.
    """
    if ip:
        cmd = f"curl -s http://ip-api.com/json/{ip}"
    else:
        cmd = "curl -s http://ip-api.com/json/"

#    await run_bash_command(cmd)

