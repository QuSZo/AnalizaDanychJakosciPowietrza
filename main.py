from flask import Flask, render_template, request, make_response
from dataAnalysis import data_analysis, data_analysis_comparison

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return (render_template('index.html'))

@app.route('/all', methods=['GET', 'POST'])
def index0():
    if request.method == 'POST':
        try:
            days = int(request.form['days'])
            if days <= 0:
                raise ValueError("Liczba dni musi być dodatnia.")

            images = data_analysis(days)
            return render_template('index.html', images=images, days=days)
        except ValueError as e:
            return render_template('index.html', error=str(e))

    return (render_template('index.html'))


@app.route('/comparison', methods=['POST'])
def index1():
    if request.method == 'POST':
        try:
            allMonths = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
            month = request.form['month']
            if month not in allMonths:
                raise ValueError("Nie ma takiego miesiąca")

            images = data_analysis_comparison()
            return render_template('index.html', images=images)
        except ValueError as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)