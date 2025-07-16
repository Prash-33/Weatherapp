from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "1c5c9f2929255117e5886bd4acc764b9"

@app.template_filter('datetimefilter')
def datetimefilter(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast_data = []
    if request.method == "POST":
        city = request.form.get("city")
        print(f"🔍 City entered: {city}")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        print(f"🌐 Requesting: {url}")

        response = requests.get(url)
        print(f"📦 Status: {response.status_code}")
        print(f"📋 Response: {response.text}")

        if response.status_code == 200:
            weather = response.json()

            forecast_response = requests.get(forecast_url)
            if forecast_response.status_code == 200:
                forecast_json = forecast_response.json()
                for item in forecast_json["list"]:
                    if "12:00:00" in item["dt_txt"]:
                        forecast_data.append({
                            "date": item["dt_txt"].split(" ")[0],
                            "temp": item["main"]["temp"],
                            "description": item["weather"][0]["description"],
                            "icon": item["weather"][0]["icon"]
                        })
        else:
            weather = {"error": "City not found!"}

    return render_template("index.html", weather=weather, forecast=forecast_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)