import pwnagotchi.plugins as plugins
import logging
import pwnagotchi
from gpiozero import Button
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts


##########################
##    SET GPIO BELOW    ##
##########################
gpioPin = 27
held_for = 0.0
modeSwitch = 'AUTO'
modeNow = 'MANU'
statusText = False
modeText = False
button = Button(gpioPin, hold_time=1.0, hold_repeat=True)


class OneButton(plugins.Plugin):

    __author__ = 'fishgrind.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'One button to rule them all \n\n 1-5s -> Restart Auto \n\n 5-10s -> Restart man \n\n 10-15s -> Restart Pi \n\n 15s+ -> Shutdown Pi'

    def on_loaded(self):
        logging.info('One Button -> Plugin loaded (GPIO %d)', gpioPin)

    def on_ready(self, agent):
        global modeNow
        global modeSwitch
        if agent.mode == 'auto':
            modeSwitch = 'MANU'
            modeNow = 'AUTO'
        else:
            modeSwitch = 'AUTO'
            modeNow = 'MANU'

    def rst(self):
        logging.info("One Button -> listening")
        global held_for
        held_for = 1.0

    def rls(self):
        global held_for
        global statusText
        global modeText
        global modeSwitch
        global modeNow
        if (held_for > 9.0):
            logging.info('One Button -> Power off')
            modeText = "ZZZZ"
            statusText = "ZZZZZ, I have been put to sleep by One Button"
            pwnagotchi.shutdown()
        elif (held_for > 4.0):
            logging.info('One Button -> rebooting')
            modeText = "BOOT"
            statusText = "Please wait, One Button is rebooting me"
            pwnagotchi.restart(modeNow)
            # pwnagotchi.reboot()
        elif (held_for > 1.0):
            logging.info('One Button -> Restart in %d', modeSwitch)
            modeText = "WAIT"
            statusText = "Please wait, One Button is switching mode"
            pwnagotchi.restart(modeSwitch)
        else:
            logging.info('One Button -> No Command')
            logging.info('One Button -> %d', modeSwitch)

    def hld(self):
        global held_for
        held_for = max(held_for, button.held_time + button.hold_time + 1)

    def on_ui_setup(self, ui):
        ui.add_element('onebuttonStatus',
                       LabeledValue(
                           color=BLACK,
                           label='OB',
                           value='',
                           position=(ui.width() - 42, ui.height() - 13),
                           label_font=fonts.Bold,
                           text_font=fonts.Medium
                       ))

    def on_rebooting(self, agent):
        logging.info("One Button -> rebooting")
        display = agent.view()
        display.update(force=True)

    def on_ui_update(self, ui):
        if statusText:
            ui.update(
                force=True,
                new_data={
                    'status': statusText,
                    'mode': modeText
                })

            with ui._lock:
                ui.remove_element('bluetooth')
                ui.remove_element('memtemp')
                ui.remove_element('latitude')
                ui.remove_element('longitude')
                ui.remove_element('altitude')
                ui.remove_element('aps')
                ui.remove_element('channel')
                ui.remove_element('uptime')

    button.when_pressed = rst
    button.when_held = hld
    button.when_released = rls
