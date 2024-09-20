import json

from playwright.sync_api import Page, Browser, BrowserContext


def save_data_to_file(data: dict) -> None:
    with open("playwright/.auth/data.json", "w") as file:
        json.dump(data, file, indent=4)


def load_data_from_file() -> dict:
    with open("playwright/.auth/data.json", "r") as file:
        data = json.load(file)
    return data

def get_page(browser: Browser, data: dict) -> tuple[Page, BrowserContext]:
    context = browser.new_context(storage_state="playwright/.auth/state.json")
    page = context.new_page()
    page.goto(data['current_url'])

    return page, context
