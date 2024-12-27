from flask import Flask, render_template, request, jsonify
import tradingeconomics as te

app = Flask(__name__)

def fetch_gdp_data_by_group(country):
    te.login("2510c8ddd52a4ab:jy8495z9kaad9ai")
    data = te.getHistoricalData(country=country, indicator='gdp')
    print(data)
    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    countries = request.json.get("countries", [])
    data = {}
    for country in countries:
        raw_data = fetch_gdp_data_by_group(country)
        processed_data = [{"DateTime": item["DateTime"], "Value": item["Value"]}
                          for item in raw_data if item["Value"] is not None]
        data[country] = processed_data
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
