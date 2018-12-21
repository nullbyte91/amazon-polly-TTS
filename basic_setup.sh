#!/bin/bash

gStreamer="libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good 
            gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc 
            gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-pulseaudio"
            
#MainStarts Here
systemBasicUpdate

function installrequirements()
{
    pip install -r requirements.txt --user
}
function systemBasicUpdate()
{
	echo "#### Basic ubuntu update"
	# Update the apt package index and Upgrade the Ubuntu system
	sudo apt-get update && sudo apt-get -y upgrade

	#Install Git
	echo "#### Install gStreamer to play audio"
	for pkg in $gStreamer; do
        	if dpkg --get-selections | grep -q "^$pkg[[:space:]]*install$" >/dev/null; then
                	echo -e "$pkg is already installed"
		else
			if sudo apt-get -qq install $pkg; then
    				echo "Successfully installed $pkg"
			else
    				echo "Error installing $pkg"
			fi
		fi
	done
}

#MainStarts 
systemBasicUpdate
installrequirements