# pwnagotchi

Just my custom pwnagotchi plugins

# Onebutton.py

- Copy to custom plugin directory
- ssh into the pi and run: `sudo apt install python3-gpiozero`
- Make sure you have push button soldered on or plugged on the GPIO-27 / pin 13 and ground, or change the gpio pin in the config (https://pinout.xyz/pinout/io_pi_zero)
- 1 to 5 seconds -> changes mode
- 6 to 10 seconds -> restarts pwnagotch (not a reboot) if you would like to reboot comment out line 62 and enable line 63 (pwnagotchi.restart(modeNow) => pwnagotchi.reboot())
- more than 10 seconds shuts down the pwnagotchi

I am not a python programmer so if you feel things could be written better, send a pr
