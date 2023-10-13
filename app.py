
from flask import render_template


from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

import subprocess
from flask import Flask, send_file
import PyPDF2
import io

UPLOAD_FOLDER = 'pdfs'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
@app.route('/', methods=['GET', 'POST'])
def upload_file():
if request.method == 'POST':
   # check if the post request has the file part
   if 'file' not in request.files:
	   return redirect(request.url)
   file = request.files['file']
   # if user does not select file, browser also
   # submit an empty part without filename
   if file.filename == '':
	   return redirect(request.url)
   if file and allowed_file(file.filename):
	   filename = secure_filename(file.filename)
	   file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	   return redirect(url_for('uploaded_file', filename=filename))
return '''
<!doctype html>
<title>Upload a PDF</title>
<h1>Upload a PDF</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form>
'''"""

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return render_template('index.html')

@app.route('/<pdf_name>/<page_range>')
def serve_pdf_pages(pdf_name, page_range):
	try:
		start_page, end_page = map(int, page_range.split('-'))
	except ValueError:
		return 'Invalid page range. Please specify the page range as two numbers separated by a dash.'

	try:
		#print(f'test {subprocess.check_output(["ls","pdfs/"])}')
		with open(f'pdfs/{pdf_name}', 'rb') as f:
			print('file opened successfully')
			reader = PyPDF2.PdfReader(f)
			print('reader successful')
			writer = PyPDF2.PdfWriter()
			print('writer successful')
			for i in range(start_page - 1, end_page):
				print(f"page:{i} loading...")
				writer.add_page(reader.pages[i])
			print('pages loaded')
			pdf_bytes = io.BytesIO()
			writer.write(pdf_bytes)
			pdf_bytes.seek(0)

		return send_file(pdf_bytes, mimetype='application/pdf')
	except FileNotFoundError:
		return f'PDF file {pdf_name} not found.'
	except Exception as e:
		return f'Unable to read PDF file. Please make sure the file is a valid PDF: {e}'
	except IndexError:
		return 'One or more of the specified pages do not exist in the PDF file.'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return 'Uploaded: ' + filename

if __name__ == '__main__':
	app.run(port=6001,debug=True)
