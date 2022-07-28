# import asyncio
import os

class Playwright:

  def __init__(self, page):
    self.page = page  # Playwright page object


  async def navigate(self, url:str):
    await self.page.goto(url)

  
  async def save_screenshots(self, div_ids:list, is_nsfw:bool):
    # For NSFW posts
    if is_nsfw:
      await self.page.locator('button:has-text("Yes")').click()
      await self.page.locator('button:has-text("Click to see nsfw")').click()

    print("Saving screenshots...")
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    for idx, id in enumerate(div_ids):
      await self.page.locator(f"div#{id}").screenshot(path=f"{self.dir_path}/temp/ss_{idx}.png")

