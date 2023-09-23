from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import subprocess
from django.http import HttpResponse
#from scrapy.crawler import CrawlerProcess
from Star_Scrapper.Star_Scrapper.spiders import books
import pymongo
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.template.loader import get_template
from django.template import Context
from django.http import FileResponse
from xhtml2pdf import pisa

# Create your views here.
uri = "mongodb+srv://Mohd_Uwaish_Scrapy:QzcG8c9LOMWoqeHp@cluster0.olcx7kr.mongodb.net/"# URI here
client = pymongo.MongoClient(uri)
db = client.Star_Scrapper
url_g=None
def home(request):
    report= False
    return render(request,"WebScoutApp/home.html", {"report":report})

def scrape(request):
    if request.method == 'POST':
        # Get the URL input from the form
        url = request.POST.get('url')
        global url_g 
        url_g = url
        print(url)

        # Replace 'run_spider.bat' with the actual path to your modified batch script
        script_path = r'C:\Users\Mohd Uwaish\Desktop\ME\DataScience\WebScout\run_spider.bat' #PATH HERE
       
        # Run the batch script and pass the URL as an argument
        result = subprocess.run([script_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Script ran")


        # Check the return code to determine success or failure
        if result.returncode == 0:
            # Batch script executed successfully
            output = f'Spider has been run successfully.\n\n{result.stdout}'
            #get_book_prices()
            report = True
            messages.success(request, 'Scraping is completed, Kindly go to Generate Report to view detaild visualization report.')

            # Redirect to the homepage
            return redirect('home:home')
        
        else:
            # Batch script encountered an error
            error_message = f'Error running spider:\n\n{result.stderr}'
            return HttpResponse(error_message)

    return render(request, 'home.html')

def get_book_prices(request):
    # Connect to your MongoDB cluster (replace with your connection details)

    # Replace 'books' with your actual collection name
    url=request.post.get("url")
    collection_name = url.split("/")[6]
    collection = db[collection_name]

    # Fetch book prices
    book_titles = [doc['Title'] for doc in collection.find({}, {'Title': 1})]
    #Fetch Rating
    book_rating = [doc['Rating'] for doc in collection.find({}, {'Rating': 1})]
    # Fetch book prices
    book_prices = [float(doc['Price'][1:]) for doc in collection.find({}, {'Price': 1})]
    #Fetch inStock
    book_inStock = [doc['inStock'] for doc in collection.find({}, {'inStock': 1})]
    #Fetch Date
    book_date = [doc['date'] for doc in collection.find({}, {'date': 1})]

    return book_prices

def list_db(request):
    collection_names = db.list_collection_names()
    return render(request, 'db_list.html', {"collection_names": collection_names})

def report(request, collection_name):
    # Connect to MongoDB
    #collection_name = url_g.split("/")[6]
    collection = db[collection_name]
    #collection =db['travel_2']

    rating_mapping = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
    df = pd.DataFrame(list(collection.find()))

    # Apply the rating mapping to the 'Rating' column
    df['Rating'] = df['Rating'].apply(lambda x: rating_mapping.get(x, 0))

    # Convert the 'Price' column to numeric values
    df['Price'] = df['Price'].apply(lambda x: float(x[1:]))

    # Extract individual fields
    book_titles = df['Title'].tolist()
    book_rating = df['Rating'].tolist()
    book_prices = df['Price'].tolist()
    book_inStock = df['inStock'].tolist()
    book_date = df['date'].tolist()
    lis = [i for i in range(1,len(book_titles)+1)]

     # Generate Price Distribution Histogram-----------1
    #fig = px.histogram(df, x=book_prices)
    fig = px.scatter(
        df,
        x=lis, 
        y=book_prices,
        color=book_prices, 
        size=book_rating,
        hover_name=book_titles, 
        hover_data=[book_prices, lis],
        title='Bubble Plot of Book Prices Over Time'
    )
    fig.update_traces(
    hovertemplate='%{text}' + '<br>Price: %{customdata[0]}<br>Book no: %{customdata[1]}',
    text=book_titles
   )
    fig.update_yaxes(title_text="Price")
    fig.update_xaxes(title_text="Book Number")
    plot_div = fig.to_html(full_html=False)

    # Count the number of in-stock and out-of-stock books-------------------2
    in_stock_count = collection.count_documents({"inStock": True})
    out_of_stock_count = collection.count_documents({"inStock": False})
    # Create a pie chart
    labels = ['In-Stock', 'Out-of-Stock']
    values = [in_stock_count, out_of_stock_count]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Convert the chart to HTML
    chart_div_2 = fig.to_html(full_html=False)


    #Price vs. Rating Scatter Plot--------------------3
    fig = px.scatter(
        df, 
        x=book_prices, 
        y=book_rating, 
        color = book_rating,
        size = book_prices,
        hover_name=book_titles, 
        hover_data=[book_prices, book_rating],
        title='Price vs. Rating Scatter Plot'
    )
    fig.update_traces(
    hovertemplate='%{text}' + '<br>Price: %{customdata[0]}<br>Book Rating: %{customdata[1]}',
    
   )
    fig.update_yaxes(title_text="Rating")
    fig.update_xaxes(title_text="Price (Euro)")
    # Convert the chart to HTML
    chart_div_3 = fig.to_html(full_html=False)


    # TOp rated books---------------------------------4
    # Find the top-rated books based on ratings
    top_rated_books_df = df[df['Rating'] == df['Rating'].max()]
    top_rated_books = top_rated_books_df.to_dict(orient='records')

    # Word CLoud----------------------------------5
    all_titles = ' '.join(book_titles)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)  
    image_stream = io.BytesIO()
    wordcloud.to_image().save(image_stream, format="PNG")
    wordcloud_image = base64.b64encode(image_stream.getvalue()).decode("utf-8")  


    context = {
        'plot_div': plot_div, 
        'chart_div_2': chart_div_2,
        'chart_div_3': chart_div_3,
        'top_rated_books': top_rated_books,
        'wordcloud_image': wordcloud_image,
        'collection_name':collection_name,

    }
    generate_report_html(context)
    return render(request, 'report.html', context)

def generate_report_html(context):
    # Render the report template with the provided context
    template = get_template('report.html')
    html = template.render(context)
    return html

def export_pdf(request):
    # Generate HTML content for the report using a Django template
    context = {}  # Provide the appropriate context here
    report_html = render(request, 'report.html', context).content.decode('utf-8')

    # Create a PDF buffer
    buffer = io.BytesIO()

    # Create the PDF document using reportlab
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Write the HTML content to the PDF
    c.drawString(100, height - 100, report_html)

    # Save the PDF content
    c.showPage()
    c.save()

    # Reset the buffer's position to the beginning
    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, as_attachment=True, filename='report.pdf')
    return response


    