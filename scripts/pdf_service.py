import subprocess
from flask import Flask, send_file
import PyPDF2
import io

app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(port=6002, debug=True)
