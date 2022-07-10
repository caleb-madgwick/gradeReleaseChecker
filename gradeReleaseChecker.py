# */30 * * * * ~/opt/anaconda3/envs/myenv/bin/python ~/PycharmProjects/gradeReleaseChecker/gradeReleaseChecker.py

import smtplib
import ssl
import time
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def main():

    # student records log in details
    username = "STUDENT\ecs_username" #todo change to ecs username
    password = "password" #todo change to ecs password

    # Setup Chrome web driver, making headless run
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("~/Documents/webDrivers/chromedriver", options=options) #todo change to absolute path of chromedriver
    driver.get("https://www.wgtn.ac.nz/student-records")

    # allow time to load page
    time.sleep(1)

    # input username, password and then submit
    username_textbox = driver.find_element(By.ID, "userNameInput")
    username_textbox.send_keys(username)
    password_textbox = driver.find_element(By.ID, "passwordInput")
    password_textbox.send_keys(password)
    login_button = driver.find_element(By.ID, "submitButton")
    login_button.submit()

    # allow time to load page
    time.sleep(1)

    # navigate to academic history upon login
    student_records = driver.find_element(By.LINK_TEXT, "Academic History")
    student_records.click()

    # allow time to load page
    time.sleep(1)

    # load the 7th table (may be differnt for other users)
    tables = driver.find_elements(By.CLASS_NAME, "datadisplaytable")[7]

    # get the rows in the table
    rows = tables.find_elements(By.TAG_NAME, "tr")

    # array to collect grades found in table
    current_grades = []

    # excluding first row, iterate table finding if grades have been inputted
    for x in range(len(rows)):
        if x != 0:
            course = rows[x].find_elements(By.TAG_NAME, "td")[0]
            grade = rows[x].find_elements(By.TAG_NAME, "td")[6]
            if grade.text != " ":
                out = course.text + ": " + grade.text
                current_grades.append(out)

    # file is stored with current cached grades
    grades_path = "~/PycharmProjects/gradeReleaseChecker/grades2022.txt" #todo change to absolute path of file
    grades_file = open(grades_path, "r")
    grades = grades_file.read()
    grades2022 = grades.split(",")
    grades_file.close()

    # if the new grades are differnt to cached grades then update and send email informing change
    if current_grades != grades2022:
        grades2022 = current_grades
        file_object = open(grades_path, 'w') 
        file_object.write(",".join(grades2022))
        file_object.close()
        send_email(grades2022)


def send_email(grades):
    # Define email sender and receiver
    email_sender = 'email_sender' #todo change to email sender
    email_password = 'email_password' #todo change to email password
    email_receiver = 'email_receiver' #todo change to email receiver

    # Set the subject and body of the email
    subject = 'Final Grade Released'
    body = "Kia Ora,\n\nYou are receiving this email as you have received a new final grade via Student Records " \
           "within the past 30 minutes. Visit https://www.wgtn.ac.nz/student-records or see below for all current " \
           "grades for this year: \n\n" + "\n".join(grades) + "\n\nKind regards,\nCaleb's Automation"

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
