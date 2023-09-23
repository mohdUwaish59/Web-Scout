@echo "off"

rem Replace 'C:\path\to\your\virtualenv\Scripts\activate' with the actual path to your virtual environment's 'activate' script.
call C:\Users\Mohd Uwaish\Desktop\ME\DataScience\WebScout\WebScout_Env\Scripts\activate

rem Navigate to the directory where your Scrapy project is located
cd /d C:\Users\Mohd Uwaish\Desktop\ME\DataScience\WebScout\Star_Scrapper\Star_Scrapper

rem Run the Scrapy spider with the specified URL
scrapy crawl books -a start_url=%1

rem Deactivate the virtual environment when done (optional)
deactivate
