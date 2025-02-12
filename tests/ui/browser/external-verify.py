import os
from subprocess import check_output
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import Page, expect


# To run this test manually:
# - Run: repo2docker tests/ui/browser/
# - Run: TEST_REPO2DOCKER_URL=<connection-url> python -mpytest --browser=firefox tests/ui/browser/external-verify.py [--headed]
def test_user_interfaces(page: Page) -> None:
    url = os.getenv("TEST_REPO2DOCKER_URL")
    u = urlsplit(url)

    # Includes token
    page.goto(url)

    # Initial page should be Jupyter Notebook
    page.wait_for_url(f"{u.scheme}://{u.netloc}/tree")

    # Check JupyterLab
    page.goto(f"{u.scheme}://{u.netloc}/lab")
    expect(page.get_by_text("Python 3 (ipykernel)").nth(1)).to_be_visible()

    # Check JupyterLab RStudio launcher
    with page.expect_popup() as page1_info:
        page.get_by_text("RStudio [↗]").click()
    page1 = page1_info.value
    page1.wait_for_url(f"{u.scheme}://{u.netloc}/rstudio/")
    # Top-left logo
    expect(page1.locator("#rstudio_rstudio_logo")).to_be_visible()
    # Initial RStudio console text
    expect(page1.get_by_text("R version ")).to_be_visible()

    # Check JupyterLab RShiny launcher
    with page.expect_popup() as page2_info:
        page.get_by_text("Shiny [↗]").click()
    page2 = page2_info.value
    page2.wait_for_url(f"{u.scheme}://{u.netloc}/shiny/")
    expect(page2.get_by_text("Index of /")).to_be_visible()
