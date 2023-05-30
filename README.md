# Containerization tools test
*Created and used for sake of master thesis at Wrocław University of Science and Technology*

Goal of this repository is phoronix-test-suite tests automation using Ansible for performance comparison of Docker and Podman.
Tests are performed on hosts defined in `inv.yml` inventory file and collected into `results` directory.

## Prerequisites
### Host node
Ansible installed with collections from `requirements.yml` file.
```
ansible-galaxy install -r requirements.yml
```
### Test nodes
Python interpreter (for Ansible), Docker and Podman installed.

## Run tests
Create inventory file and add hosts:
```
cp inv.example.yml inv.yml
```
Run playbook:
```
ansible-playbook playbook.yml
```

