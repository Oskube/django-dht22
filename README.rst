DHT22 View
==========

Simple app to log serial input to a django database. Views generate a line chart from the data and JSON output for other purposes. This can be also easily modified to other similar applications.

Serial input is expected to have a baud rate of 9600 and the string expected should be formatted as "HUMIDITY;TEMPERATURE".

App name says 'dht22' but you can use other sensors instead as long as the input string is formatted as expected.

Quick start
-----------

1. Add "dht22" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'dht22',
    ]

2. Include the dht22 URLconf in your project urls.py like this:

        url(r'^dht22/', include('dht22.urls')),

3. Run `python manage.py migrate` to create the database models.

4. Open your crontab with `crontab -e` and add the line below into it. Change path to your django project and port to the device which provides the serial input. Make sure that your user has access to the serial port, this can be done by adding the user to 'dialout' group.

    `*/5 * * * * python3 /path/to/djangoproject/manage.py readserial <port>`

    If you are using virtual env use:

    `*/5 * * * * /path/to/virtualenv/bin/python3 /path/to/djangoproject/manage.py readserial <port>`

5.  Start the development server and visit http://127.0.0.1:8000/dht22/ to see temperature and humidity chart.
