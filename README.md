# Sunfounder Super Kit Python code for Raspberry Pi

Website:
	www.sunfounder.com

E-mail:
	support@sunfounder.com

### Customer's idea:
 - [**pimorse**](https://github.com/gabolander/pimorse) Raspberry Pi Morse code generater from [Gabriele Zappi](https://github.com/gabolander) Run command `git submodule update --init` to clone the pymorse submodule, or else, it will be empty.

----------

### 2016/01/13 update
Summery:
- Fix a bug on `05_rgb.py`

Details:
- Thanks for zygotine (We don't have his/her name, it's from his/her email address), fix the setColor function.


### 2015/12/28 update
Summary:
- Remove `01_led_1.py`
- Rename `01_led_2.py` to `01_led.py`
- Remove `02_btnAndLed_1.py`
- Rename `02_btnAndLed_2.py` to `02_btnAndLed.py`
- Rearrange `04_pwmLed.py`

Details:
- For `01_led_1.py` and `01_led_2.py`, they are the same but with different coding structions. we remove the _1 and remane the _2 for the simillar struction. (Also see `02_btnAndLed_1.py` and `02_btnAndLed_2.py`)
- For `04_pwmLed.py`, we rearrange the structions also for the simillar struction.

### 2015/06/12 update
For 13_lcd1602: fix some bug for some Raspberry Pi B+.
- Change pins:
 - RS =====> 27
 - EN =====> 22
 - D4 =====> 25
 - D5 =====> 24
 - D6 =====> 23
 - D7 =====> 18
