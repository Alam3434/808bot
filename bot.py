from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import smtplib, ssl
from email.message import EmailMessage
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time


# Specify the URL of the website
def run_bot():
    uri = "mongodb+srv://mohammadalam2003:alam343@cluster0.n7l3iee.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["808bot"]
    collection = db["808bot"]

    url = "https://888lots.com/login/login"  

    user = "zsadistribution@gmail.com"
    password = "Clip78@0"
    driver = webdriver.Chrome()
    # Navigate to the website
    driver.get(url)

    driver.implicitly_wait(3)
    html = driver.page_source

    email_input= driver.find_element(By.CSS_SELECTOR, "#input-email")
    pass_input = driver.find_element(By.CSS_SELECTOR, "#input-password")

    email_input.send_keys(user)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    watchlist = driver.find_element(By.CSS_SELECTOR, "#headers > div.header-top.compact-hidden > div > div > div.header-top-right.collapsed-block.col-sm-12.col-md-7.col-xs-12.pr-0 > div > ul > li.wishlist.hidden-xs > a")
    watchlist.click()

    pagination = driver.find_element(By.CLASS_NAME, "pagination")
    pages = pagination.find_elements(By.TAG_NAME, 'li')
    counter = 0

    for i in range(1,len(pages)-1):
        driver.get(f"https://888lots.com/watchlist?page={i}")
        table = driver.find_element(By.CSS_SELECTOR, "#vue-app > div.main-container.container > div > div:nth-child(4) > div:nth-child(2) > div.table-responsive > table")
        rows = table.find_elements(By.TAG_NAME, 'tr')
        items = []
        final_posts = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            counter+=1
            post = {}
            for i in range(len(cells)):
                if i==2:
                    post["_id"] = cells[i].text
                elif i== 3: 
                    post["name"] = cells[i].text
                elif i== 4: 
                    post["stock"] = cells[i].text
                elif i== 3: 
                    post["price"] = cells[i].text
            already_item = collection.find({"_id": cells[2].text})
            if len(list(already_item)) == 0:
                final_posts.append(post)
            else:
                for item in already_item:
                    if already_item["stock"] == "Out Of Stock" and post["stock"] != "Out Of Stock":
                        collection.update_one({"_id": already_item["_id"]}, {"$set": {"stock": post["stock"]}})
                        items.append(post["name"])
        if final_posts:
            collection.insert_many(final_posts)
    return items
def send_message(items):
    if not items:
        return 
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port
    sender_email = "burneralam@gmail.com"
    receiver_email = "aamiyo2003@gmail.com"
    password = "icgu zuqh azcg bmyf"
    subject = "Test Email"
    body = f"This is a test email sent from Python. {items}"

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send the email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.send_message(msg)
total_sleep_time = 5 * 60 * 60
while True:
    items = run_bot()
    send_message(items)
    time.sleep(total_sleep_time)
    