It contains Fullstack Nano Degree projects of database and applications.

## File structure
- `Vagrantfile`: Configuration file to install vertual machine, The Vagrant VM, which includes PostgreSQL
- `tournament`: A PostgreSQL project
- `sqlalchemy_sample`: A sqlalchemy project
- `webserver`: BaseHTTPServer project, using sqlalchemy
- `flask`: Flask framework project


## Setup
1. Power up the VM and log in to the VM.
Run the following in the directory where Vagrantfile locates:
```
vagrant up
vagrant ssh
```

## Vagrantfile
port forwarding
```
Vagrant.configure("2") do |config|
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  ...
end
```
And it handles vagrant installation.
