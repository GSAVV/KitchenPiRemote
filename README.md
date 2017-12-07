# KitchenPiRemote
Remote control for my RasPi in the kitchen

The following steps are important for the configuration of the KitchenPi

## Load the program from this repository
```
mkdir ~/Scripts/
cd ~/Scripts/
git clone https://github.com/GSAVV/KitchenPiRemote
sudo chmod 770 StartScript.sh
```

## Configure the autostart of the python script
add the following line

`@/home/pi/Scripts/KitchenPiRemote/StartScript.sh`

in this file

~/.config/lxsession/LXDE-pi/autostart

## Configure xpdf
add the following lines
```
initialZoom width
continuousView yes
```
in this file

/etc/xpdf/xpdfrc

and add the following lines
```
<application class="Xpdf" name="win">
      <fullscreen>yes</fullscreen>
    </application>
  </applications>
```
in this file 

~/.config/openbox/lxde-pi-rc.xml

## Rotate Desktop
add the following line
```
display_rotate=1
```
in this file

/boot/config.txt


## Samba Share
```
sudo mkdir /home/pi/Recipes
sudo chown root:users /home/pi/Recipes
sudo chmod 770 /home/pi/Recipes
sudo apt-get update
sudo apt-get install samba samba-common smbclient
sudo smbpasswd -a pi
sudo smbpasswd -a root
```

and add this lines
```
[Recipes]
   comment = Recipes for the KitchenPi
   path = /home/pi/Recipes
   browsable = yes
   read only = no
```
to this file

sudo nano /etc/samba/smb.conf



