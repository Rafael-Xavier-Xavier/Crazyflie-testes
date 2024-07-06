# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
This script shows the basic use of the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

The MotionCommander uses velocity setpoints.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper

URI ='radio://0/90/2M/E7E7E7E701'

logging.basicConfig(level=logging.ERROR)

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Abaixo a definição das funções de movimento do CrazyRover:

def Forward(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 1)
    cf.param.set_value(wheels + '.' + pwm_1, 50)
    cf.param.set_value(wheels + '.' + pwm_2, 50)

def Backward(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 4)
    cf.param.set_value(wheels + '.' + pwm_1, 200)
    cf.param.set_value(wheels + '.' + pwm_2, 200)

def Turnleftcfront(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 1)
    cf.param.set_value(wheels + '.' + pwm_1, 50)
    cf.param.set_value(wheels + '.' + pwm_2, 250)

def Turnrigtfront(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 1)
    cf.param.set_value(wheels + '.' + pwm_1, 250)
    cf.param.set_value(wheels + '.' + pwm_2, 50)

def Turnleftcback(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 4)
    cf.param.set_value(wheels + '.' + pwm_1, 50)
    cf.param.set_value(wheels + '.' + pwm_2, 225)

def Turnrigtback(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 4)
    cf.param.set_value(wheels + '.' + pwm_1, 225)
    cf.param.set_value(wheels + '.' + pwm_2, 50)

def Spinright(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 3)
    cf.param.set_value(wheels + '.' + pwm_1, 225)
    cf.param.set_value(wheels + '.' + pwm_2, 50)

def Spinleft(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 2)
    cf.param.set_value(wheels + '.' + pwm_1, 50)
    cf.param.set_value(wheels + '.' + pwm_2, 225)

def Stop(scf, wheels, state, pwm_1, pwm_2):
    cf = scf.cf
    wheels # = group1
    state # = name1
    pwm_1 # = name2
    pwm_2 # = name3

    cf.param.set_value(wheels + '.' + state, 4)
    cf.param.set_value(wheels + '.' + pwm_1, 0)
    cf.param.set_value(wheels + '.' + pwm_2, 0)


# Parte do Log (Estudar e ver o que é realmente necessário incluir no código). 

def param_stab_est_callback(name, value):
    print('The crazyflie has parameter ' + name + ' set at number: ' + value)
x = 1

def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()

def simple_log(scf, logconf):

    with SyncLogger(scf, lg_stab) as logger:

        for log_entry in logger:

            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))

            break


def simple_connect():

    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")

# Até aqui sobre a parte do Log.

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

#    lg_stab = LogConfig(name='Wheels', period_in_ms=10)
#    lg_stab.add_variable('wheels.state', 'float')
#    lg_stab.add_variable('wheels.pwm_1', 'float')
#    lg_stab.add_variable('wheels.pwm_2', 'float')
    
#    a = 'wheels'
#    b = 'state'
#    c = 'pwm_1'
#    d = 'pwm_2'

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        Spinright(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Spinleft(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Forward(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Backward(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Turnleftcfront(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Turnrigtfront(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Turnleftcback(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Turnrigtback(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
        Stop(scf, 'wheels', 'state', 'pwm_1', 'pwm_2')
        time.sleep(1)
