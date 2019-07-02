import http
import socket

from selenium.webdriver.remote.command import Command

def driverStatus(driver):
    try:
        driver.execute(Command.STATUS)
        return "Alive"
    except (socket.error, http.client.CannotSendRequest):
        return "Dead"