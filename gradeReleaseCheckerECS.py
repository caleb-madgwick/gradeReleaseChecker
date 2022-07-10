import smtplib
import ssl
import time
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def main():

    # student records log in details
    username = ""
    password = ""

    # Setup Chrome web driver, making headless run
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("~/Documents/webDrivers/chromedriver", options=options)
    driver.get("https://apps.ecs.vuw.ac.nz/cgi-bin/studentmarks?current-year=1")

    # allow time to load page
    time.sleep(1)

    # input username, password and then submit
    username_textbox = driver.find_element(By.NAME, "username")
    username_textbox.send_keys(username)
    password_textbox = driver.find_element(By.NAME, "password")
    password_textbox.send_keys(password)
    password_textbox.send_keys(Keys.RETURN)


    # allow time to load page
    time.sleep(3)

    tables = driver.find_element(By.CLASS_NAME, "tab-content")

    rows = tables.find_elements(By.CLASS_NAME, "tab-pane")

    current_grades = []

    for select in rows:
        driver.execute_script("arguments[0].setAttribute('class', 'active')", select)
        course = select.find_element(By.TAG_NAME, "h3")
        grades = select.find_elements(By.CLASS_NAME, "panel-success")
        print(course.text[0:7] + ": " + str(len(grades)))
        current_grades.append(course.text[0:7] + ": " + str(len(grades)))

    grade_path = "~/PycharmProjects/gradeReleaseChecker/ECSgrades2022.txt"
    grades_file = open(grade_path, "r")
    grades = grades_file.read()
    grades2022 = grades.split(",")
    grades_file.close()

    if current_grades != grades2022:
        grades2022 = current_grades
        file_object = open(grade_path, 'w')
        file_object.write(",".join(grades2022))
        file_object.close()
        send_email()


def send_email():
    # Define email sender and receiver
    email_sender = ''
    email_password = ''
    email_receiver = ''

    # Set the subject and body of the email
    subject = 'ECS Grade Released'
    body = "Kia Ora,\n\nYou are receiving this email as you have received a new grade via the ECS system" \
           "within the past 30 minutes. Visit https://apps.ecs.vuw.ac.nz/cgi-bin/studentmarks?current-year=1 " \
           "to view the new grade \n\nKind regards,\nCaleb's Automation"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



if __name__ == "__main__":
    main()
