"""
Сценарий 2 (headless) — автоматизация поиска видео на VK Видео.

Шаги:
1. Открыть главную страницу VK Видео
2. Ввести поисковый запрос в строку поиска
3. Выполнить поиск
4. Перейти на первое видео из выдачи
5. Сохранить скриншот и HTML страницы с видео
"""

import re
from pathlib import Path

from playwright.sync_api import Page, expect

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
SEARCH_QUERY = "Python programming tutorial"


def test_search_and_open_video(page: Page) -> None:
    """Поиск видео на VK Видео и переход на первый результат."""
    ARTIFACTS_DIR.mkdir(exist_ok=True)

    # 1. Открываем главную страницу VK Видео
    page.goto("https://vk.com/video", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.screenshot(path=str(ARTIFACTS_DIR / "01_main_page.png"), full_page=False)

    # 2-3. Вводим поисковый запрос и выполняем поиск
    search_input = page.locator('input[type="search"], input[placeholder*="Поиск"], input[placeholder*="Search"], input.search, input[name="q"]').first
    search_input.click()
    search_input.fill(SEARCH_QUERY)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(ARTIFACTS_DIR / "02_search_results.png"), full_page=False)

    # 4. Переходим на первое видео из выдачи
    first_video = page.locator('a[href*="/video"][href*="-"]').first
    first_video.click()
    page.wait_for_timeout(3000)

    # 5. Сохраняем скриншот и HTML страницы с видео
    page.screenshot(path=str(ARTIFACTS_DIR / "03_video_page.png"), full_page=False)

    html_content = page.content()
    (ARTIFACTS_DIR / "03_video_page.html").write_text(html_content, encoding="utf-8")

    # Проверяем, что мы на странице видео
    assert "video" in page.url.lower(), f"Expected video URL, got: {page.url}"
