from playwright.sync_api import sync_playwright

LOGIN_URL = "https://demorealcoderz.skilla.ai/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False so you can watch
    page = browser.new_page()

    print("=" * 50)
    print("QR Login Page - Basic Tests")
    print("=" * 50)

    # ────────────────────────────────────────
    # TEST 1: Page Loads Successfully
    # ─────────────────────────────────────────
    print("\n[TEST 1] Checking if page loads...")
    response = page.goto(LOGIN_URL, wait_until="networkidle")

    if response and response.status == 200:
        print("  PASS - Page loaded successfully (status 200)")
    else:
        print(f"  FAIL - Page did not load properly (status: {response.status if response else 'unknown'})")

    print("  Page Title:", page.title())
    print("  Current URL:", page.url)

    # ─────────────────────────────────────────
    # TEST 2: Check Login Form Elements Exist
    # ─────────────────────────────────────────
    print("\n[TEST 2] Checking login form elements...")

    # Common selectors for username/email field
    email_selectors = [
        'input[type="email"]',
        'input[name="email"]',
        'input[name="username"]',
        'input[id*="email"]',
        'input[id*="user"]',
        'input[placeholder*="mail"]',
        'input[type="text"]',
    ]

    # Common selectors for password field
    password_selectors = [
        'input[type="password"]',
        'input[name="password"]',
        'input[id*="pass"]',
        'input[placeholder*="assword"]',
    ]

    # Common selectors for submit button
    button_selectors = [
        'button[type="submit"]',
       
    ]

    # Find email/username field
    email_field = None
    for sel in email_selectors:
        if page.locator(sel).count() > 0:
            email_field = sel
            print(f"  PASS - Email/Username field found: {sel}")
            break
    if not email_field:
        print("  WARN - Email/Username field not found with common selectors")

    # Find password field
    password_field = None
    for sel in password_selectors:
        if page.locator(sel).count() > 0:
            password_field = sel
            print(f"  PASS - Password field found: {sel}")
            break
    if not password_field:
        print("  WARN - Password field not found")

    # Find submit button
    submit_button = None
    for sel in button_selectors:
        if page.locator(sel).count() > 0:
            submit_button = sel
            print(f"  PASS - Submit button found: {sel}")
            break
    if not submit_button:
        print("  WARN - Submit button not found with common selectors")

    # ─────────────────────────────────────────
    # TEST 3: Empty Form Submission (Validation)
    # Check that the form shows errors on empty submit
    # ─────────────────────────────────────────
    print("\n[TEST 3] Testing empty form submission (validation)...")
    if submit_button:
        page.locator(submit_button).click()
        page.wait_for_timeout(1500)  # wait 1.5 seconds for validation to appear

        # Check if URL changed (it should NOT change on empty submit)
        if page.url == LOGIN_URL or "auth" in page.url:
            print("  PASS - Page did not navigate away (form validation working)")
        else:
            print("  WARN - Page navigated away on empty submit:", page.url)
    else:
        print("  SKIP - No submit button found")

    # ─────────────────────────────────────────
    # TEST 4: Wrong Credentials
    # Check that login fails with fake credentials
    # ─────────────────────────────────────────
    print("\n[TEST 4] Testing login with wrong credentials...")

    # Reload fresh page
    page.goto(LOGIN_URL, wait_until="networkidle")

    if email_field and password_field and submit_button:
        page.locator(email_field).fill("wronguser@test.com")
        page.locator(password_field).fill("WrongPassword123")
        page.locator(submit_button).click()
        page.wait_for_timeout(2000)  # wait for error message

        # Check if still on login page (should be)
        if "auth" in page.url or page.url == LOGIN_URL:
            print("  PASS - Wrong credentials did not log in (still on auth page)")
        else:
            print("  WARN - Page navigated away with wrong credentials:", page.url)
    else:
        print("  SKIP - Required form fields not found")
        
        # ─────────────────────────────────────────
    # TEST 6: Screenshot of Current State
    # ─────────────────────────────────────────
    print("\n[TEST 6] Taking screenshot...")
    page.screenshot(path="QR/login_page.png", full_page=True)
    print("  Screenshot saved: QR/login_page.png")
    

    # ─────────────────────────────────────────
    # TEST 5: Valid Credentials Login
    # ─────────────────────────────────────────
    print("\n[TEST 5] Testing login with valid credentials...")

    VALID_EMAIL = "shrivastavaharshwardhan@gmail.com"
    VALID_PASSWORD = "RC521"

    page.goto(LOGIN_URL, wait_until="networkidle")

    if email_field and password_field and submit_button:
        page.locator(email_field).first.fill(VALID_EMAIL)
        page.locator(password_field).first.fill(VALID_PASSWORD)
        page.locator(submit_button).click()
        page.wait_for_timeout(3000)

        if page.url != LOGIN_URL and "login" not in page.url:
            print("  PASS - Login successful, navigated to:", page.url)
        else:
            print("  FAIL - Login failed, still on login page:", page.url)
    else:
        print("  SKIP - Required form fields not found")

    # ─────────────────────────────────────────
    # TEST 6: Screenshot of Current State
    # ─────────────────────────────────────────
    print("\n[TEST 6] Taking screenshot...")
    page.screenshot(path="QR/login_page.png", full_page=True)
    print("  Screenshot saved: QR/login_page.png")
    

    # ─────────────────────────────────────────
    # TEST 6: Page Responsiveness (Mobile View)
    # ─────────────────────────────────────────
    # print("\n[TEST 6] Checking mobile view...")
    # page.set_viewport_size({"width": 375, "height": 812})  # iPhone size
    # page.goto(LOGIN_URL, wait_until="networkidle")
    # page.wait_for_timeout(1000)
    # page.screenshot(path="QR/login_mobile.png", full_page=True)
    # print("  PASS - Mobile view loaded")
    # print("  Screenshot saved: QR/login_mobile.png")

    # Reset to desktop
    page.set_viewport_size({"width": 1280, "height": 720})

    # ─────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("Screenshots saved in QR/ folder")
    print("=" * 50)

    browser.close()
