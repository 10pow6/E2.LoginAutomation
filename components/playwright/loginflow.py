from playwright.async_api import async_playwright
from components.helpers import helpers

class playwright_flows:
    @staticmethod
    async def execute_e2_login( tui_context, username, password, otp, target):
        async with async_playwright() as p:
            #headless=True to set as headless mode
            helpers.fitted_log_msg( tui_context=tui_context, text=["Opening Playwright browser in (non) headless mode"] )

            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto( target )
            helpers.fitted_log_msg( tui_context=tui_context, text=["Navigating to " +  target] )

            # Click on login button
            await page.get_by_text('LOG IN / SIGN UP').click()
            helpers.fitted_log_msg( tui_context=tui_context, text=["Clicking login"] )

            # Fill in the username and password fields and click the login button
            await page.locator('[name=username]').fill(username)
            await page.locator('[name=password]').fill(password)
            helpers.fitted_log_msg( tui_context=tui_context, text=["Filling user & pass on Auth0 Login page"] )

            await page.locator('[name=action]').click()
            helpers.fitted_log_msg( tui_context=tui_context, text=["Clicking login"] )

            # Fill in the OTP field and click the login button
            await page.locator('[name=otp_token]').fill(otp)
            await page.locator('//button[text()="Log in"]').click()
            helpers.fitted_log_msg( tui_context=tui_context, text=["Sending OTP code and clicking log in"] )

            # Wait for the Raid span to be visible
            await page.locator("//span[@class='hidden lg:inline' and text()='Raid']").wait_for()
            
            # Get the cookies and return them as a string
            cookies = await context.cookies()
            selected_cookies = [cookie for cookie in cookies if '.earth2.io' in cookie['domain']]
            cookie_string = '; '.join([cookie['name'] + '=' + cookie['value'] for cookie in selected_cookies])
            helpers.fitted_log_msg( tui_context=tui_context, text=["Getting cookies","Cookie set"] )
            # prints sensitive information
            # fitted_log_msg( self, text=["Cookie result: ", cookie_string] )
            helpers.fitted_log_msg( tui_context=tui_context, text=["Closing out Playwright browser"] )
            
            # Close the browser
            await browser.close()