#!/usr/bin/env python3

import subprocess
import json

def app():
    project_dir = f"{'/'.join(__file__.split('/')[:-2])}"
    command = f"{project_dir}/venv/bin/python3 {project_dir}/inventories/maas.py --list"
    try:
        result = subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

    old_dict = json.loads(result)
    #os_controllers = old_dict["controlplane"]["hosts"]
    #kube_control_plane = 

    all_hosts_dict = {}

    for k,v in old_dict["_meta"]["hostvars"].items():
        if k in old_dict["controlplane"]["hosts"]:
            all_hosts_dict[k] = v 
            all_hosts_dict[k]["etcd_member_name"] = k.split(".")[0]
            
    general_hosts = {}
    
    for host in old_dict["controlplane"]["hosts"]:
        general_hosts[host] = None


    #print(all_hosts_dict)

    new_dict = {
        "all": { "hosts": all_hosts_dict, "vars": {"ansible_user": "ubuntu", "ansible_ssh_common_args": "-o UserKnownHostsFile=/dev/null" }},
        "kube_control_plane": {"hosts": general_hosts},
        "etcd": {"hosts": general_hosts},
        "kube_node": {"hosts": general_hosts}
    }
    print(json.dumps(new_dict, indent=4))

if __name__ == "__main__":
    app()
