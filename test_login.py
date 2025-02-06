from playwright.sync_api import Page, expect
import re
import time

def test_login_validUser(page: Page):
    page.goto('https://www.saucedemo.com/v1/')
    expect(page.locator('.login_logo')).to_be_in_viewport()
    page.get_by_placeholder("Username").fill('standard_user')
    page.locator("[data-test='password']").fill("secret_sauce")
    expect(page.locator("[class='bot_column']")).to_be_in_viewport()
    page.locator('.btn_action').click()
    expect(page).to_have_url(re.compile('https://www.saucedemo.com/v1/inventory.html'))

def test_login_lockedoutUser(page: Page):
    page.goto('https://www.saucedemo.com/v1/')
    expect(page.locator('.login_logo')).to_be_in_viewport()
    page.get_by_placeholder("Username").fill('locked_out_user')
    page.locator("[data-test='password']").fill("secret_sauce")
    expect(page.locator("[class='bot_column']")).to_be_in_viewport()
    page.locator('.btn_action').click()
    expect(page.locator('[data-test="error"]')).to_be_visible()

def test_login_problem_user(page: Page):
    page.goto('https://www.saucedemo.com/v1/')
    expect(page.locator('.login_logo')).to_be_in_viewport()
    page.get_by_placeholder("Username").fill('problem_user')
    page.locator("[data-test='password']").fill("secret_sauce")
    expect(page.locator("[class='bot_column']")).to_be_in_viewport()
    page.locator('.btn_action').click()    
    errors_messages = []
    page.on("console", lambda msg: errors_messages.append(msg.text) if msg.type == "error" else None)
    expect(page).to_have_url(re.compile('https://www.saucedemo.com/v1/inventory.html'))
    length_errors = len(errors_messages)
    print("Captured Console Errors:", errors_messages)
    assert length_errors > 0  


def test_performance_glitch(page: Page):
    page.goto('https://www.saucedemo.com/v1/')
    expect(page.locator('.login_logo')).to_be_in_viewport()
    page.get_by_placeholder("Username").fill('performance_glitch_user')
    page.locator("[data-test='password']").fill("secret_sauce")
    expect(page.locator("[class='bot_column']")).to_be_in_viewport()
    page.locator('.btn_action').click()
    start_loading_time = time.time()
    expect(page).to_have_url(re.compile('https://www.saucedemo.com/v1/inventory.html'))
    end_loading_time = time.time()
    performance_time = round(end_loading_time - start_loading_time, 2)
    assert performance_time > 5