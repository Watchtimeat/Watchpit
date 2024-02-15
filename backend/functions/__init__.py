from time import sleep


def loopback(**kwargs):
    if "exception" in kwargs:
        raise Exception(kwargs["exception"])
    if "sleep" in kwargs:
        sleep(int(kwargs["sleep"]))
    return kwargs
