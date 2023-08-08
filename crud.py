
@app.route('/upload', methods=['POST'])
def upload_pdf():
    global filename_id
    pdf_file = request.files['pdf_file']
    if pdf_file:
        # Get the filename
        filename = pdf_file.filename
        # Save the uploaded file on the server
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        pdf_file.save(pdf_path)
        print(f"Uploading pdf to server: {pdf_path}")
        # Upload to collection
        try:
            upsert_rsp = collection.upsert_file(pdf_path)
        except Exception as e:
            print(f'Error on {pdf_path}: {e}')
        doc_id = upsert_rsp.ids[0]
        dcl =  collection.get_doc(doc_id)
        text_len = len(" ".join([dc.text for dc in dcl]))
        title = dcl[0].metadata.title if dcl[0].metadata.title else "Unknown Title"        
        print(f'Processed {filename}: "{title}"  {text_len//1024} KB text ({len(dcl)} chunks)')
        # Add the filename to the list
        doc_chunks, next_index = collection.get_doc_chunks()
        filename_id = [(doc_chunk[0].metadata.source_id, doc_chunk[0].metadata.document_id) for doc_chunk in doc_chunks]
        return index()  # Redirect back to the index page

@app.route('/process', methods=['POST'])
def process_pdf():
    selected_file = request.form['selected_file']
    return f"Processing selected file: {selected_file}"

@app.route('/process_text', methods=['POST'])
def process_text():
    input_text = request.form['input_text']
    return render_template('index.html', fnames=fnames, processed_text=processed_text)
