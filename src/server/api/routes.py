from flask import render_template, request

receipts = []
current_id = 1

def register_routes(app):
    @app.route('/receipts/all', methods=['GET'])
    def list_receipts():
        return render_template('index.html', receipts=receipts)

    @app.route('/add_receipt/upload', methods=['GET', 'POST'])
    def create_receipt_data():
        global current_id
        if request.method == 'POST':
            title = request.form.get('title')
            author = request.form.get('author')
            if not title or not author:
                return 'Missing Data', 400
            receipt = {'id': current_id, 'title': title, 'author': author}
            receipts.append(receipt)
            current_id += 1
            return render_template('index.html', receipts=receipts)
        return render_template('form.html')