#!/usr/bin/env bash

sudo systemctl stop lcdd lcdproc g15ctrld
sudo systemctl start lcdd lcdproc g15ctrld

sleep 1

exec conky -c "$HOME/.config/conky/conky_for_lcd/conky_for_lcd.conf" \
     | python3 "/home/somnodeus/.config/0_my/my_lcd_client.py"