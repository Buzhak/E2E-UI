import os
from playwright.sync_api import Page, expect

from .constants import (
    CURRENT_URL,
    LOGIN_PAGE
)


def test_full_process(page: Page):
    '''
    Тест для проверки сценария покупки товара на сайте saucedemo.com
    '''

    page.goto(LOGIN_PAGE)

    # Login
    login = page.get_by_placeholder('Username')
    expect(login, CURRENT_URL.format(page.url)).to_be_visible()
    login.fill(os.getenv('login', 'standard_user'))

    password = page.get_by_placeholder('Password')
    expect(password, CURRENT_URL.format(page.url)).to_be_visible()
    password.fill(os.getenv('password', 'secret_sauce'))

    button = page.get_by_text('Login')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Add item to cart
    item = page.locator('.inventory_item').nth(0)
    expect(item, CURRENT_URL.format(page.url)).to_be_visible()

    button = item.get_by_role('button', name='Add to cart')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Go to cart
    button = page.locator('.shopping_cart_badge')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Cart checout
    button = page.get_by_role('button', name='Checkout')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Cart checout step 1
    page.get_by_placeholder('First Name').fill('first_name')
    page.get_by_placeholder('Last Name').fill('last_name')
    page.get_by_placeholder('Zip/Postal Code').fill('0000')

    button = page.get_by_text('Continue')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Cart checout step 2
    button = page.get_by_role('button', name='Finish')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()

    # Finish
    button = page.get_by_role('button', name='Back Home')
    expect(button, CURRENT_URL.format(page.url)).to_be_visible()
    button.click()
