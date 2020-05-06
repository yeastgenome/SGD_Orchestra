# SGD_Orchestra

This SGD Containerization repository. SGD project is split between Backend repository and Frontend respository. The main goal is to containerize the whole project.

## Backend Project Stack

- Redis
- Nginx
- Postgres database
- Pyramid Framework(ORM + REST API)
  - Jinja templates
- Elasticsearch Analytics Engine
- Curator Interface frontend(Internal use only)
 -React app

## Frontend Project Stack

- Redis
- Nginx
- Javascript
  - Combination of react components and vaniala javascript
- HTML + Foundation framework
- Pyramid Framework(ORM + REST API)
  - Jinja templates

## Docker

### Elasticsearch & Dockerswarm

- We will eventually move to kubernetes but for now we're experimenting with dockerswarm for our elasticsearch analytics engine.

#### Capacity Planning

- We are using t3.2xlarge instances to host our docker containers. See specs below for the planned infrastructure which is subject to change since we're still experimenting.
  - 3 Master Nodes
  - 2 Data Nodes
  - 2 Coordination Nodes
  - 2 Ingest Nodes

#### EC2 Provisioning

- There are several ways to do this. We are going to use docker-machine utility. Docker machine help to provision and manage docker hosts, EC2 instances in this case. For more information see [docker doc](https://docs.docker.com/machine/overview/)
- Before provisioning EC2, take note of what region and instance type to run the elasticsearch service.
- To provision EC2 instance, run the following command

```bash
docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type t2.medium --amazonec2-security-group your-sec-group --amazonec2-open-port 9200/tcp --amazonec2-open-port 9300/tcp --amazonec2-open-port 2377/tcp --amazonec2-open-port 7946/tcp --amazonec2-open-port 4789/udp --amazonec2-open-port 7946/udp es-01

##### SSH into docker-machine provisioned instance
- ``` docker-machine create ``` command creates a new private-public key pair each time it runs. It would be nice if docker-machine worked with pem files. Future docker-machine PR was opened about this last we checked. in the mean time you would have to use privete keys to ssh, move with caution with that approach.
- To get EC2 machine private key do the following:

```bash
docker-machine ls # lists ec2 instances you created using docker-machine
docker-machine inspect {EC2_Machine_name}
```

- You will get  response that looks like below after running the second command above

```json
{
    "ConfigVersion": 3,
    "Driver": {
        "IPAddress": "111.111.111.1",
        "MachineName": "my_machine_05",
        "SSHUser": "ubuntu",
        "SSHPort": 22,
        "SSHKeyPath": "path_to_key/id_rsa",
        "StorePath": "/Users/uname/.docker/machine",
        "SwarmMaster": false,
        "SwarmHost": "tcp://0.0.0.0:3376",
        "SwarmDiscovery": "",
        "Id": "xxxxx",
        "AccessKey": "",
        "SecretKey": "",
        "SessionToken": "",
        "Region": "us-west-2",
        ...
    }
}

```

#### EC2 Configurations

- You might have encountered this memory issue before if you have setup an elasticsearch cluster before but essentially the computer(s) complain about not having enough virtual memory for elasticsearch. The following fixes that issue and we set it up to prevent from happening in the first place. For more information check this [article][https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html]

Run the following command using docker-machine and setup virtual memory on each of the machines we provisioned.

```bash
# this modifies the /etc/sysctl.conf file
docker-machine ssh my_machine_05 sudo sysctl -w vm.max_map_count=262144

# --------------------------- OR --------------------------

# to add permanently run the following
docker-machine ssh my_machine_05 sudo "sed -i 'a vm\.max_map_count=262144' /etc/sysctl.conf"

```

Run the following to modify memlock for docker. Setting memlock will sure there's always shared memory pool and doesn't get paged out.

```bash
docker-machine ssh my_machine_05 sudo "sed -i '/ExecStart=\/usr\/bin\/dockerd/ s/$/--default-ulimit memlock=-1/' /etc/systemd/system/docker.service.d/10-machine.conf"

```

#### Create Docker Swarm Cluster

- Firstly run ``` eval ``` command with your machine of choosing to act as master for the cluster. The eval command execute arguments as shell a command. In this case every command will run inside the current terminal or command line session as the machine chosen to be master. It's possible to change to another machine anytime.

```bash
eval $(docker-machine env my_machine_05)

```

- Secondly, initiate docker swarm

```bash
docker swarm init
```

You will get out output that looks like the following:

```text
Swarm initialized: current node (bla bla bla) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-bla-bla@ip-address

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

#### Add worker nodes to the docker swarm

```bash
docker-machine ssh my_machine_04 sudo docker swarm join --token SWMTKN-bla-bla@ip-address
```

- Add all the required nodes to the swarm cluster
- Check the list of nodes in the created cluster

```bash
docker node ls
```

- For fail safe practice, add more manager nodes. Odd number of nodes is recommended in case one node fails, the remaining nodes can handle main manager node duties

```bash
docker node promote my_machine_3 my_machine_2
```

#### Confifure Elasticsearch nodes(containers)

- We create 3-primary containers, 4-data containers, 2-coordniator containers, 2-ingest containers
- We add other services like 1-kibana containers, traefik and visualizer containers

#### Elasticsearch File Structure

|-- ./configs


#### Deploy & Run elasticsearch service

- Run the following command to start the elasticsearch cluster
- More information on deploying start in this [article](https://docs.docker.com/engine/reference/commandline/stack_deploy/)

```bash
docker stack deploy -c elastic-stack.yml elastic

```

### Create EC2 instance using python

- [Guide doc](https://blog.ipswitch.com/how-to-create-an-ec2-instance-with-python)
- [Another useful guide](https://stackabuse.com/automating-aws-ec2-management-with-python-and-boto3/)
