# anomaly

```
cmk@raspberrypi:~ $ cat /etc/xdg/lxsession/LXDE-pi/autostart 
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@sh /home/cmk/Documents/anomaly/anomaly.sh
xrandr -o 3
```
