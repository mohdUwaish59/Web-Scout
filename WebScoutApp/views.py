from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import subprocess
from django.http import HttpResponse
#from scrapy.crawler import CrawlerProcess
from Star_Scrapper.Star_Scrapper.spiders import books

# Periodic deletion code
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
#ended

# Create your views here.
def home(request):
    return render(request,"WebScoutApp/home.html")

def scrape(request):
    if request.method == 'POST':
        # Get the URL input from the form
        url = request.POST.get('url')

        # Replace 'run_spider.bat' with the actual path to your modified batch script
        script_path = r'{PATH TO FILE}'

        # Run the batch script and pass the URL as an argument
        result = subprocess.run([script_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check the return code to determine success or failure
        if result.returncode == 0:
            # Batch script executed successfully
            output = f'Spider has been run successfully.\n\n{result.stdout}'
            return HttpResponse(output)
        else:
            # Batch script encountered an error
            error_message = f'Error running spider:\n\n{result.stderr}'
            return HttpResponse(error_message)

    return render(request, 'home.html')
    