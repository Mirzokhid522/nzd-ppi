from playwright.sync_api import sync_playwright
import time
import os

def run_ppi_workflow():
    project_folder = os.path.abspath(os.path.dirname(__file__))
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            print("Navigating to Infoshare Stats NZ...")
            page.goto("https://infoshare.stats.govt.nz/", timeout=60000)
            
            # Navigate tree structure for PPI
            page.wait_for_selector("text=Economic indicators", timeout=15000)
            print("Expanding 'Economic indicators'...")
            page.click("text=Economic indicators")
            
            ppi_selector = "text=Producers Price Index - PPI"
            page.wait_for_selector(ppi_selector, state="visible", timeout=15000)
            print("Clicking 'Producers Price Index - PPI'...")
            page.click(ppi_selector, force=True)
            
            print("Waiting for PPI sub-options to load...")
            target_link = "Outputs (ANZSIC06) - NZSIOC level 1, percentage change, Base: Dec. 2010 qtr"
            page.wait_for_selector(f"text={target_link}", timeout=20000)
            
            print(f"Clicking headline table: '{target_link}'...")
            page.click(f"text={target_link}", force=True)
            
            # Wait for variable configuration page to load
            print("Waiting for variable selection screen...")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Automatically click all "Select all" links
            print("Automatically selecting all variables and full time history...")
            select_all_links = page.locator("text=Select all").all()
            for link in select_all_links:
                try:
                    link.click()
                    time.sleep(0.3)
                except:
                    pass

            print("\n" + "="*65)
            print(" [READY] Automation complete up to the export screen!")
            print(" 1. Scroll down to the bottom right dropdown in the browser.")
            print(" 2. Change 'Table on screen' to 'Comma delimited (.csv)'.")
            print(" 3. Click 'Go'. Playwright will capture it automatically as ppi.csv!")
            print("="*65 + "\n")

            # Listen for the download event when you click Go manually
            with page.expect_download(timeout=180000) as download_info:
                print("Waiting for you to change format to CSV and click 'Go'...")
            
            download = download_info.value
            
            # Save it explicitly as ppi.csv right in your project folder
            final_file_path = os.path.join(project_folder, "ppi.csv")
            download.save_as(final_file_path)
            
            print(f"\n[SUCCESS] PPI File successfully captured and saved to: {final_file_path}")
            time.sleep(3)

        except Exception as e:
            print(f"\n[ERROR] Step failed: {e}")
        
        finally:
            browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    run_ppi_workflow()