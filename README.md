# xiaomi-Bluetooth-themometer
Xiaomi temperature humidity sensor

This is a little script in order to read temperature and humidity from Xiaomi sensor.

*Note* Make sure that gatttool and expect are installed. 

'''
$ ./xiaomi.exp 4C:65:A8:DA:F3:B1
T=19.1 H=40.9 B=99%
'''

*T* is the temparature in celsius. 

*H* is humidity in percent 

*B* is the battery level in percent.

## *Note*
There is also a script written in Python. That was my first try. I recommend to use the script based on expect since it is faster and more stable.
