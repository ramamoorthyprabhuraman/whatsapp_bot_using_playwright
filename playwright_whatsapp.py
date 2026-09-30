from datetime import datetime
from playwright.sync_api import sync_playwright

USER_DATA_DIR = "./whatsapp_user_data"

print("Starting the Playwright script on Windows...")
print(f"Current date and time: {datetime.now()}")

with sync_playwright() as p:
    # 1. Launch persistent context (Windows Chromium)
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        no_viewport=True,
        args=["--start-maximized"],
    )

    page = context.pages[0] if context.pages else context.new_page()

    # 2. Open WhatsApp Web
    print("Opening WhatsApp Web...")
    page.goto("https://web.whatsapp.com")

    # 3. Wait for chat list pane to mount
    print("Waiting for WhatsApp UI to load...")
    page.locator("#pane-side").wait_for(state="attached", timeout=60000)
    print("WhatsApp interface loaded successfully.")

    # 4. Dismiss any 'What's new' / sync banners
    try:
        modal_btn = page.locator(
            'div[role="dialog"] button:has-text("OK"), '
            'div[role="dialog"] button:has-text("Got it"), '
            'div[role="dialog"] button:has-text("Continue"), '
            'div[role="dialog"] [aria-label="Close"]'
        )
        if modal_btn.is_visible(timeout=2000):
            modal_btn.click()
            print("Dismissed modal popup.")
    except Exception:
        pass

    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # 5. Activate & focus the Search Bar
    # In current WhatsApp Web, the search container is a button/box that activates upon click
    print("Activating search box...")
    search_trigger = page.locator(
        'button[aria-label*="Search"], '
        'div[aria-label*="Search"], '
        '#side [role="button"], '
        '#side [role="textbox"], '
        '#side [contenteditable="true"]'
    ).first

    search_trigger.click()
    page.wait_for_timeout(500)

    # Windows native WhatsApp shortcut to guarantee focus
    page.keyboard.press("Control+Alt+/")
    page.wait_for_timeout(500)

    # Clear any leftover query and type Priya
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type("Priya", delay=40)
    print("Typed 'Priya' into search.")

    # 6. Wait for search results and open Priya's chat
    page.wait_for_timeout(2000)

    priya_contact = page.locator(
        '#pane-side span[title="Priya"], '
        '#pane-side span:text-is("Priya"), '
        'span[title="Priya"]'
    ).first

    if priya_contact.is_visible(timeout=2000):
        priya_contact.click()
        print("Clicked on Priya from search results.")
    else:
        # If the search results pane auto-highlights the first match, press Enter to open
        print("Opening top match via Enter...")
        page.keyboard.press("Enter")

    # 7. Locate Message Box & Send text
    print("Waiting for chat input box...")
    # The active message box is the last visible contenteditable area in footer/main
    message_input = page.locator(
        'footer div[contenteditable="true"], '
        'div[role="textbox"][aria-label*="Type a message"], '
        'div[role="textbox"][data-tab="10"]'
    ).last

    message_input.wait_for(state="visible", timeout=10000)
    message_input.click()

    message = "Hello Priya, this is a test message sent using Playwright!"
    page.keyboard.type(message, delay=15)
    page.keyboard.press("Enter")
    print(f"Message sent: {message}")

    # Allow 2 seconds for delivery ticks to render before screenshot
    page.wait_for_timeout(2000)

    # 8. Screenshot & Exit
    page.screenshot(path="message_sent_to_Priya.png")
    print("Screenshot saved as message_sent_to_Priya.png")

    context.close()
    print("Browser closed. Script completed successfully.")