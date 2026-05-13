import sys
import os
import time
import json
from selenium.webdriver.common.by import By

# Add doctoexam to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from automation.browser import create_driver, login, navigate_to_add_question, quit_driver

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Force headless off so you can see the screen
    config['automation']['headless_mode'] = False
    
    print("Launching browser...")
    driver = create_driver(config)
    try:
        print("Navigating to login page...")
        driver.get(config['website']['login_url'])
        
        print("\n" + "="*60)
        print("🛑 ACTION REQUIRED:")
        print("Please log in manually on the browser window that just opened.")
        print("Solve any CAPTCHAs if necessary.")
        print("Navigate to the 'Add Question' page.")
        print("Once the final 'Add Question' form is completely visible on screen,")
        input("PRESS ENTER HERE IN THIS TERMINAL TO SCAN THE DOM...")
        print("="*60 + "\n")
        
        os.makedirs('output', exist_ok=True)
        with open('output/page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        print("\n--- DOM SCAN RESULTS ---")
        print("Page source saved to output/page_source.html")
        
        print("\n[ BUTTONS ]")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for b in buttons:
            text = b.text.strip()
            if text:
                print(f"Text: '{text}' | id: '{b.get_attribute('id')}' | class: '{b.get_attribute('class')}'")
                
        print("\n[ INPUTS ]")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for i in inputs:
            print(f"name: '{i.get_attribute('name')}' | id: '{i.get_attribute('id')}' | type: '{i.get_attribute('type')}' | class: '{i.get_attribute('class')}'")
            
        print("\n[ SELECTS (Dropdowns) ]")
        selects = driver.find_elements(By.TAG_NAME, "select")
        for s in selects:
            print(f"name: '{s.get_attribute('name')}' | id: '{s.get_attribute('id')}' | class: '{s.get_attribute('class')}'")

        print("\n[ TEXTAREAS ]")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        for t in textareas:
            print(f"name: '{t.get_attribute('name')}' | id: '{t.get_attribute('id')}' | class: '{t.get_attribute('class')}'")

    finally:
        quit_driver(driver)

if __name__ == '__main__':
    main()