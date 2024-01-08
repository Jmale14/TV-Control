#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from cec_ctl_class import cec_ctl


def main(args):
    #stream = os.popen('ls -la')
    #output = stream.readlines()
    #print(output)
    
    #x = subprocess.run(['ls', '-la'])
    #print(x)
    
    tv_cntrl = cec_ctl(verbose=True)
    time.sleep(10)
    tv_cntrl.standby()
    
    time.sleep(10)
    
    tv_cntrl.power_on()
    
    
    tv_cntrl.mute()

    #tv_cntrl.volume_up()

    #tv_cntrl.volume_down()

    #tv_cntrl.channel_up()

    #tv_cntrl.channel_down()
    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
