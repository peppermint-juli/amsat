sudo cat <<EOF > /etc/NetworkManager/system-connections/usb0.nmconnection
[connection]
id=usb0
type=ethernet
interface-name=usb0
autoconnect=true

[ipv4]
method=manual
addresses=169.254.1.1/16

[ipv6]
method=ignore
EOF

sudo chmod 600 /etc/NetworkManager/system-connections/usb0.nmconnection
sudo chown root:root /etc/NetworkManager/system-connections/usb0.nmconnection
sudo nmcli connection reload
sudo nmcli connection modify usb0 connection.autoconnect yes
sudo nmcli connection modify usb0 connection.interface-name usb0

echo Setup Complete!


