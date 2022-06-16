from pandas import read_excel  # Solo nos traemos lo estrictamente necesario
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
from datetime import date
import os, sys, datetime
from selenium.webdriver.chrome.options import Options
from email.mime.multipart import MIMEMultipart
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from selenium.webdriver.chrome.options import Options