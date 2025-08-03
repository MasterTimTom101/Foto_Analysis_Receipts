from flask import render_template, request

receipts = []
current_id = 1

def register_routes(app):
    @app.route('/receipts/home', methods=['GET'])
    def list_info():
        return render_template('index.html', receipts=receipts)

    @app.route('/receipts/about', methods=['GET'])
    def list_about_info():
        return render_template('about.html', receipts=receipts)

    @app.route('/receipts/show', methods=['GET'])
    def list_receipts():
        return render_template('show.html', receipts=receipts)

    @app.route('/receipts/upload', methods=['GET', 'POST'])
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
        return render_template('upload.html')

    @app.route('/receipts/analyse', methods=['GET', 'POST'])
    def create_analysis_data():
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
        return render_template('analyse.html')

    @app.route('/receipts/result_out', methods=['GET', 'POST'])
    def create_result_data():
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
        return render_template('result_output.html')