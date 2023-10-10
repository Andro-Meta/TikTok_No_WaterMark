from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import logging

# Constants
TIK_WM_URL = 'https://www.tikwm.com/'
HD_DOWNLOAD_XPATH = '//a[contains(text(), "No Watermark(HD) .mp4")]'
MP3_DOWNLOAD_XPATH = '//a[contains(text(), "Music .mp3")]'
LOG_FILENAME = 'app.log'

# Set up logging
logging.basicConfig(filename=LOG_FILENAME, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def download_tiktok_content(url: str, choice: str, driver: webdriver.Chrome) -> None:
    try:
        # Extract username and video number from the URL
        parts = url.split("/")
        username = parts[3][1:]  # Extract the username
        video_number = parts[5].split('?')[0]  # Extract the video number
        filename = f'{username}_{video_number}'

        # Navigate to the new website
        driver.get(TIK_WM_URL)
        
        # Wait for the input field to be present, and enter the URL
        input_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="url"]'))
        )
        input_field.send_keys(url)
        print("URL entered")
        
        # Find the submit button next to the input field and click it
        submit_button = driver.find_element(By.XPATH, '//button[contains(text(), "Download")]')
        submit_button.click()
        print("Submit button clicked")
        
        # Wait for a bit to ensure the download buttons have loaded
        time.sleep(5)  # Adjust this sleep time if necessary
        
        if choice == '1':
            # Wait for the download button for HD video to be clickable
            download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, HD_DOWNLOAD_XPATH))
            )
            print("HD download button found")
            file_extension = 'mp4'
        elif choice == '2':
            # Wait for the download button for mp3 to be clickable
            download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, MP3_DOWNLOAD_XPATH))
            )
            print("MP3 download button found")
            file_extension = 'mp3'
        else:
            print("Invalid choice, exiting.")
            return
        
        # Get the download URL
        content_url = download_button.get_attribute('href')
        
        # Download the content
        response = requests.get(content_url)
        with open(f'{filename}.{file_extension}', 'wb') as file:
            file.write(response.content)
        print(f'Content downloaded successfully as {filename}.{file_extension}.')

    except Exception as e:
        logging.error(f"An error occurred in download_tiktok_content: {e}")

def main():
    url = input("Enter the TikTok video URL: ")
    choice = input("Enter 1 for video, 2 for mp3: ")

    chrome_options = Options()
    # Comment out the headless mode for troubleshooting
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # WebDriver instance for downloading content
    driver = webdriver.Chrome(options=chrome_options)
    download_tiktok_content(url, choice, driver)
    # Explicitly quit the driver after downloading content
    driver.quit()

if __name__ == "__main__":
    main()
