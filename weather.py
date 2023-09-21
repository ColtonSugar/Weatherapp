import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage you want to scrape
url = "https://weather.com/weather/tenday/l/Youngstown+OH?canonicalCityId=2793e44da479328c35f16aaab4bd1a229f11b2dac0caef70d1e9334fbfd08c3b"

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the <span> elements with the specified class
        temphi_spans = soup.find_all('span', class_='DetailsSummary--highTempValue--3PjlX')
        templo_spans = soup.find_all('span', class_='DetailsSummary--lowTempValue--2tesQ')
        day_spans = soup.find_all('h3', class_='DailyContent--daypartName--3emSU')
        rain_spans = soup.find_all('span', class_='DailyContent--value--1Jers')
        wind_spans = soup.find_all('span', class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers DailyContent--windValue--JPpmk')
        # Create a CSV file and write the header
        with open("Weatherfile.csv", "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Date","High Temperature", "Low Temperature", "Rain Percentage", "Wind speed and direction"])

            # Extract and write the data to the CSV file
            for day ,high, low, rain, wind in zip(day_spans,temphi_spans, templo_spans, rain_spans, wind_spans):
                date = day.text
                high_temp = high.text
                low_temp = low.text
                rain_per = rain.text
                wind_speed = wind.text
                csvwriter.writerow([date,"High", high_temp, "Low" ,low_temp,"Wind Speed/rain percentage" ,rain_per])

        print("Data has been written to Weatherfile.csv")
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")

except Exception as e:
    print("An error occurred:", str(e))
