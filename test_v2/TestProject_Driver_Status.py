import http
import socket
import time

from selenium.webdriver.remote.command import Command

def driverStatus(driver):
    try:
        driver.execute(Command.STATUS)
        driver.close()
        driver.quit()
        time.sleep(2)
        return "Alive"
    except (socket.error, http.client.CannotSendRequest):
        return "Dead"