from flask import Flask, render_template, request, send_file
from scraper import scrape_amazon
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    item_count = None
    filename = None
    if request.method == 'POST':
        product_name = request.form['product']
        filename, item_count = scrape_amazon(product_name)
    return render_template('index.html', count=item_count, file=filename)

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join("static", filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
