from playwright.sync_api import sync_playwright
from datetime import datetime


print("Starting the Playwright script...")
print(f"Current date and time: {datetime.now()}")

# WhatsApp Message Sender

# Chromium--> WhatsApp Web --> Login / QR scan --> Search "Priya"
# Open Priya chat --> Send message --> Screenshot --> Close browser


with sync_playwright() as p:

    # 1. Launch Chromium
    
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Chromium opened.")
    
    # 2. Open WhatsApp Web

    page.goto("https://web.whatsapp.com",wait_until="domcontentloaded")

    print("WhatsApp Web opened.")

    page.screenshot(path="whatsapp_web.png")


    # 3. Wait for WhatsApp login
    

    # On the first run, scan the QR code manually.
    # Once the Search box appears, login is complete.


    print("\nPlease scan the QR code if it is displayed...")

    page.wait_for_selector('input[placeholder="Search or start new chat"]',state="visible")

    print("WhatsApp login successful.")

    # 4. Search for Priya

    search_box = page.get_by_placeholder("Search or start new chat")

    search_box.click()

    search_box.fill("Priya")

    print("Searching for Priya...")

    # Wait for search results
    page.wait_for_timeout(3000)


    # 5. Select Priya

    priya = page.get_by_text("Priya",exact=True).first

    priya.wait_for(state="visible",timeout=30000)

    priya.click()

    print("Priya's chat opened.")

    page.wait_for_timeout(2000)

    # 6. Send message
   

    message = ("Hello Priya," "this is a test message sent using Playwright!")

    message_box = page.get_by_placeholder("Type a message")

    message_box.wait_for(state="visible",timeout=30000)

    message_box.click()

    message_box.fill(message)

    print(f"Sending message: {message}")

    page.wait_for_timeout(2000)

    # Press Enter to send
    message_box.press("Enter")


    page.wait_for_timeout(3000)

    print("Message sent successfully.")


    # 7. Screenshot


    page.screenshot(path="message_sent_to_Priya.png")

    print("Screenshot saved as " "message_sent_to_Priya.png")


    # 8. Close browser

    browser.close()

    print("Browser closed.")
    print("Script completed successfully.")
