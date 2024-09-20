import os
from playwright.sync_api import Page, expect, Browser
from dotenv import load_dotenv

from .constants import (
    LOGIN_PAGE,
    LOGIN_FAILED_MESSAGE,
    ELEMENTS_NOT_EXIST,
    WRONG_ITEM,
    CART_EMPTY,
    CART_NOT_EMPTY,
    FORM_FALUED,
    FORM_NOT_FALUED
)
from .functions import (
    get_page,
    load_data_from_file,
    save_data_to_file
)

load_dotenv()


def test_login(page: Page):
    '''
    Тестируем логин на сайт
    '''

    page.goto(LOGIN_PAGE)
    page.get_by_placeholder('Username').fill(os.getenv('login', 'standard_user'))
    page.get_by_placeholder('Password').fill(os.getenv('password', 'secret_sauce'))
    page.get_by_text('Login').click()

    # Проверяем что логин прошёл успешно и есть список товаров на странице
    expect(page.locator('.inventory_container'), LOGIN_FAILED_MESSAGE).to_be_visible()

    save_data_to_file({'current_url': page.url})
    page.context.storage_state(path="test/state.json")


def test_add_somesing_to_cart(browser: Browser):
    '''
    Проверяем наличие элементов товаров на странице.
    Добавляем первый товар в корзину.
    Проверяем что товар добавился.
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    items_locator = page.locator('.inventory_item')
    item_count = items_locator.count()

    # Проверяем есть ли товары на странице
    assert item_count > 0, ELEMENTS_NOT_EXIST

    first_item = items_locator.nth(0)
    first_item.get_by_role('button', name='Add to cart').click()

    # Проверяем добавляется ли товар в корзину
    expect(first_item.get_by_role('button', name='Remove'), CART_EMPTY).to_be_visible()
    expect(page.locator('.shopping_cart_badge'), CART_EMPTY).to_be_visible()

    page.context.storage_state(path="test/state.json")
    
    item_name = first_item.locator('.inventory_item_name').text_content()
    data['item_name'] = item_name
    save_data_to_file(data)
    
    context.close()


def test_checkout_card(browser: Browser):
    '''
    Переходим в корзину
    Проверяем есть ли товар в корзине
    Проверяем тот ли это товар
    Заказываем
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    page.locator('.shopping_cart_badge').click()

    # Проверяем добавился ли товар непостредственно в корзину
    cart_item = page.locator('.cart_item')
    expect(cart_item, CART_EMPTY).to_be_visible()
    
    # Проверяем тот ли это товар
    current_item_name = cart_item.locator('.inventory_item_name').text_content()
    item = data['item_name']
    assert  current_item_name == item, WRONG_ITEM.format(current_item_name, item)

    page.get_by_role('button', name='Checkout').click()

    page.context.storage_state(path="test/state.json")

    data['current_url'] = page.url
    save_data_to_file(data)

    context.close()


def test_checkout_step_one_no_fill(browser: Browser):
    '''
    Подтверждаем форму без заполнения данных
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    page.get_by_text('Continue').click()

    error_message = page.locator('.error-message-container')
    expect(error_message.locator('h3'), FORM_NOT_FALUED).to_be_visible()

    context.close()


def test_test_checkout_step_one(browser: Browser):
    '''
    Заполняем данные формы и одтверждаем
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    page.get_by_placeholder('First Name').fill('first_name')
    page.get_by_placeholder('Last Name').fill('last_name')
    page.get_by_placeholder('Zip/Postal Code').fill('0000')

    page.get_by_text('Continue').click()

    # Проверяем подтвердилась ли форма
    expect(page.locator('.checkout_summary_container'), FORM_FALUED).to_be_visible()

    page.context.storage_state(path="test/state.json")

    data['current_url'] = page.url
    save_data_to_file(data)

    context.close()


def test_test_checkout_step_two(browser: Browser):
    '''
    Проверяем тот ли товар на странице
    и завершаем вротой этап заказа.
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    # Проверяем тот ли товар на странице
    current_item_name = page.locator('.inventory_item_name').text_content()
    item = data['item_name']
    assert  current_item_name == item, WRONG_ITEM.format(current_item_name, item)

    page.get_by_role('button', name='Finish').click()

    # Убеждаемся, товар заказан успешно
    expect(page.locator('.complete-header')).to_be_visible()
    expect(page.get_by_role('button', name='Back Home')).to_be_visible()

    page.context.storage_state(path="test/state.json")

    data['current_url'] = page.url
    save_data_to_file(data)

    context.close()


def test_checkout_complete(browser: Browser):
    '''
    Заказ завершён, переходим на главную страницу,
    убеждаемся, что корзина пустая
    '''
    data = load_data_from_file()
    page, context = get_page(browser=browser, data=data)

    page.get_by_role('button', name='Back Home').click()

    page.context.storage_state(path="test/state.json")

    # проверяем что товар на странице доступен
    expect(page.locator('.inventory_item').nth(0), ELEMENTS_NOT_EXIST).to_be_visible()
    # проверяем что товаров в корзине нет
    expect(page.locator('.shopping_cart_badge'), CART_NOT_EMPTY).not_to_be_visible()

    context.close()
