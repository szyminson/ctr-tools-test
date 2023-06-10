# Containerization tools test
*Created and used for sake of master thesis at Wrocław University of Science and Technology*

Goal of this repository is phoronix-test-suite tests automation using Ansible for performance comparison of Docker and Podman.
Tests are performed on hosts defined in `inv.yml` inventory file and collected into `results` directory. After using result processing script processed results can be found in `processed` directory.

## Prerequisites
### Control node
Ansible installed with collections from `requirements.yml` file.
```
ansible-galaxy install -r requirements.yml
```
For result processing script install python requirements.
```
pip install -r requirements.txt
```
### Managed (test) nodes
Python interpreter (for Ansible), Docker and Podman installed.

## Usage
Create inventory file from example and edit it to add your own hosts.
```
cp inv.example.yml inv.yml
```
### Run tests
```
ansible-playbook playbook.yml -t tests
```
### Collect results or fetch session log
```
ansible-playbook playbook.yml -t results
```
### Abort tests
```
ansible-playbook playbook.yml -t abort
```
### Process results
```
./process_results.py
```

