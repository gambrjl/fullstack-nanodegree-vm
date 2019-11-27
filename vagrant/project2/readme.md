# Item Catalog
This repository stores all code required for the item catalog site. It uses sqlalchemy to store User, Category, and Item Information.

## Installation

Clone this repository using:

`git clone https://github.com/Seananigans/fullstack-nanodegree-vm.git`

## Requirements

### Install VirtualBox

VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the _platform package_ for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

![vagrant --version](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584881ee_screen-shot-2016-12-07-at-13.40.43/screen-shot-2016-12-07-at-13.40.43.png)

_If Vagrant is successfully installed, you will be able to run_ `vagrant --version`
_in your terminal to see the version number._
_The shell prompt in your terminal may differ. Here, the_ `$` _sign is the shell prompt._


## Usage

1. First change into the catalog directory:

	`~/fullstack/vagrant/`

2. Start the Vagrant VM

    $ vagrant up

3. ssh into vagrant machine

    $ vagrant ssh

4. Change to the correct directory

    $ cd /vagrant/project2

5.  Install Python modules needed by app

    $python3 -m pip -r req.txt

5.  Run the `app.py` file in the command line:

	`python3 app.py`

6. Open `localhost:5000/` in your browser.

7. Login:

    - Some database content has been pre-loaded into database

	a. Create your own Categories and Items.

	b. Edit/Delete your own Categories and Items.

## Author

Jamie Gambrell