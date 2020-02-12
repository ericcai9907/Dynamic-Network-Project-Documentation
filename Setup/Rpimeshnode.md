
# Mesh Node Setup Raspberry Pi

## Part 1. Create the SD card and perform initial setup

1. Download the latest Raspbian image
2. Flash the image onto a SD card
3. For headless setup, creat an empty file called "ssh" with no file extension in the /boot drive
4. Insert the SD card into the Raspberry Pi and power on
5. Default login hostname is **pi** and password is **raspberry**.
6. On the Raspberry Pi command line issue the command

    ```sudo raspi-config```

    and then go through and change the following settings:
    - Network Options > Hostname change to **rpimeshnode#** (# is the node number)
    - Localisation Options > Change Locale/Timezone/WiFi country
    - Network Option > WiFi.
    - interfacing Options > SSH/VNC, ensure SSH or VNC server is enabled

    Exit raspi-config, don't reboot yet.
7. Update the Pi using command

    ```sudo apt-get update && sudo apt-get upgrade -y```
8. Reboot

    ```sudo reboot -n```
9. Connect to the pi using SSH or VNC, the command for connection the Pi using SSH is:

    ```ssh pi@rpimeshnode#.local```

## Part 2. Install batctl

10. Install the requirements for batct

    ```sudo apt install libnl-3-dev libnl-genl-3-dev```
11. Download and install batct

    ```text
    git clone https://git.open-mesh.org/batctl.git
    cd batctl
    sudo make install
    ```

## Part 3. Setup batman-adv


12. Create a file **~/start-batman-adv.sh** with editor

    e.g.
    - ```vi ~/start-batman-adv.sh```
    - ```nano ~/start-batman-adv.sh```

    the file should contain the following:

    ```text
    #!/bin/bash
    # batman-adv interface to use
    sudo batctl ra BATMAN_V
    sudo batctl meshif bat0 if add wlan0
    sudo ifconfig bat0 mtu 1532

    # Tell batman-adv this is a gateway client
    sudo batctl meshif bat0 gw_mode client

    # Activates batman-adv interfaces
    sudo ifconfig wlan0 up
    sudo ifconfig bat0 up
    ```

13. Make the start-batman-adv.sh file executable with command :

    ```text
    chmod +x ~/start-batman-adv.sh
    ```

14. Create the network interface definition for the wlan0 interface by creating a file as root user e.g.

    - ```sudo vi /etc/network/interfaces.d/wlan0```
    - ```sudo nano /etc/network/interfaces.d/wlan0```

    then add the following content:

    ```text
    auto wlan0
    iface wlan0 inet manual
    	wireless-channel 11
    	wireless-essid senior-project-mesh
	wireless-mode ad-hoc
    ```

15. Ensure batman-adv kernel module is loaded at boot time:

    ```echo 'batman-adv' | sudo tee --append /etc/modules```

16. Stop the DHCP process from trying to manage the wireless lan interface by issuing the following command :

    ```echo 'denyinterfaces wlan0' | sudo tee --append /etc/dhcpcd.conf```

17. Make sure the startup script gets called by editing file **/etc/rc.local** as root user, e.g.

    - ```sudo vi /etc/rc.local```
    - ```sudo nano /etc/rc.local```

    and insert:

    ```/home/pi/start-batman-adv.sh &```

    before the last line: **exit 0**
18. If this pi will not be a bridge or gateway node then shut it down using command :

    ```sudo shutdown -h now```