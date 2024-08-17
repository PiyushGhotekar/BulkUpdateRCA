from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)

# Directory to save uploaded and processed files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the CSV file to remove commas
        df = pd.read_csv(file_path)
        df_no_commas = df.applymap(lambda x: str(x).replace(',', '') if isinstance(x, str) else x)
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], f'no_commas_{file.filename}')
        df_no_commas.to_csv(output_file, index=False)

        return send_file(output_file, as_attachment=True)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
