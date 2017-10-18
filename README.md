It contains Udacity projects of database and applications.

## File structure
Each folder has own README.
- `Vagrantfile`: Configuration file to install vertual machine, The Vagrant VM, which includes PostgreSQL
- `tournament`: A PostgreSQL project
- `sqlalchemy_sample`: A sqlalchemy project
- `webserver`: BaseHTTPServer project, using sqlalchemy
- `flask`: Flask framework project
- `oauth`: Sample for Google account login 


## Setup
1. Power up the VM 
Run the following in the directory where Vagrantfile locates:
```
vagrant up
```
To turn the virtual machine off type `vagrant halt`.
2. Log in to the VM.
```
vagrant ssh
```
To log out, type `exit`

It is important to turn off/log out property especially when you run vagrant in different directories.
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
