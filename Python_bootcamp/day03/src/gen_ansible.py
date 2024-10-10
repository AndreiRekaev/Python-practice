import yaml

def get_yaml_data(file_path: str):
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def ansible_install_packages_module(install_packages: list):
    tasks = []
    for package in install_packages:
        tasks.append({
            "name": f"Install {package}",
            "ansible.builtin.apt": {
                "name": package,
                "state": "latest"
            }
        })
    return tasks

def ansible_copy_files_module(files: list, file_destination: str):
    tasks = []
    for file in files:
        tasks.append({
            "name": f"Copy {file}",
            "ansible.builtin.copy": {
                "src": file,
                "dest": file_destination,
                "mode": "0644"
            }
        })
    return tasks

def ansible_run_file_module(script_path: str, bad_guys: list):
    tasks = [{
        "name": "Run script",
        "ansible.builtin.command": {
            "cmd": f"python3 {script_path}/consumer.py -e {', '.join(bad_guys)}"
        }
    }]
    return tasks

def ansible_generate_data_module(script_path: str):
    tasks = [{
        "name": "Run script for generate data",
        "ansible.builtin.command": {
            "cmd": f"python3 {script_path}/producer.py -e 2"
        }
    }]
    return tasks

def yaml_save_data(yaml_data, file_src):
    with open(file_src, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, Dumper=yaml.Dumper, sort_keys=False)

if __name__ == "__main__":
    y_data = get_yaml_data("../materials/todo.yml")

    playbook = [
        {
            "hosts": "all",
            "tasks": []
        }
    ]

    playbook[0]["tasks"].extend(ansible_install_packages_module(y_data["server"]["install_packages"]))
    playbook[0]["tasks"].extend(ansible_copy_files_module(y_data["server"]["exploit_files"], "/tmp"))
    playbook[0]["tasks"].extend(ansible_run_file_module("/tmp", y_data["bad_guys"]))
    playbook[0]["tasks"].extend(ansible_generate_data_module("/tmp"))

    yaml_save_data(playbook, "../materials/deploy.yml")
