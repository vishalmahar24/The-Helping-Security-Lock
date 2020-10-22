# helpful-security-lock
The Helping Security Lock is about enabling physically impaired people to easily enter their
home while providing a reliable and secure locking mechanism. The product could also be
used by not disabled people, who value security and are tired of carrying keys around with
them. 
We want to make the life of disabled people easier by supporting them in one of the
most trivial task in daily life. Our product is thought to be primarily for disabled people,
however it can also be used by not disabled people. We plan to make it modular, meaning
that you can choose the sensor modules which you want to have in your locking mechanism,
for example, for blind people a barcode reader is difficult to operate, as they have to position
the barcode precisely in front of the reader. Therefore they could order the product without the
barcode reader, thus making it cheaper. We estimate a cost of 7000 Rupees for the product
with all the sensor modules (Voice recognition, Face recognition, pincode,
fingerprint sensor,
barcode reader). The product could also be used for Labs at university, where only faculty
members should have access to the Lab. It would save the university money for making the
keys and especially it would prevent the university from having to change the lock if one of the
members looses his key.

# Operating System:
It is made for Raspberry pi (tested on Pi 3).

# Requirements:

1. Python2.7
2. opencv
3. zbar-py ( http://github.com/zplab/zbar-py )
4. face_recognition ( http://github.com/ageitgey/face_recognition )
5. speechpy ( http://github.com/astorfi/speechpy )
6. pydtw ( http://github.com/shunsukeaihara/pydtw )
7. pyfingerprint ( http://github.com/bastianraschke/pyfingerprint )
8. snowboy hotword detection ( http://github.com/Kitt-AI/snowboy )

# Details of Running the Codes:

To start at a specific module, change the `startMain.py` and run the `init()` function after including the desired header file.
The default pin is '1234', which can be changed while running using `#` or in the program at the beginning.
The default passkey to change a module is '62018', which was only used for demonstration purpose, as in reality, a user will only choose one module.

For the Voice+Finger Recognition module, it is assumed that the snowboy hotword detection is cloned into home directory, i.e. `/home/pi/`.
