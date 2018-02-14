# Synchronous TDOA multisensor model

This is my master gr. project.

Relies on TDOA algorithm proposed [here](https://s3-us-west-1.amazonaws.com/stevenjl-bucket/tdoa_localization.pdf).

Simple TDOA locator implemented earlier [here](https://github.com/Myshj/tdoa_localisation).

The system simulates sensor network that includes arbitrary count of sound sensors.

This network operates in an open sound propagation environment.

Information about sound events (like gunshots, explosions etc) received from sensor controllers and collected by TDOA-groups is used for tracking coordinates of such events.

System can track static sound sources as well as moving ones.

The system architecture and the obtained results were reported and discussed at the [ICCSEEA 2018](http://www.uacnconf.org/iccseea2018/index.html).
