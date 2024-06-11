# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
import logging
from flask import Flask, jsonify, request, send_from_directory
from models import Journal, JournalEntry

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# In-memory storage for journal entries
journal_entries = []
entries = []
entry_id_counter = 1


@app.route('/journals', methods=['GET'])
def get_journals():
    return jsonify([journal.to_dict() for journal in journal_entries]), 200


@app.route('/addjournal', methods=['POST'])
def add_journal():
    data = request.get_json()
    new_journal = Journal(journal_id=len(journal_entries) + 1, name=data['name'])
    journal_entries.append(new_journal)
    return jsonify(new_journal.to_dict()), 201

@app.route('/addentry', methods=['POST'])
def add_entry():
    global entry_id_counter
    data = request.form
    file = request.files.get('image')
    journal_id = int(data['journal_id'])
    logging.debug("Received request to add entry")
    logging.debug(data)
    logging.debug(journal_entries[0].journal_id)
    logging.debug(journal_id)

    journal = next((j for j in journal_entries if j.journal_id == journal_id), None)
    if journal:
        image_path = None
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)        
        new_entry = JournalEntry(
            entry_id=entry_id_counter,
            journal_id=journal_id,
            title=data['title'],
            content=data['content'],
            date=data['date'],
            image_path=image_path
        )
        logging.debug("Received request to add entry")
        entry_id_counter += 1
        entries.append(new_entry)
        return jsonify(new_entry.to_dict()), 201
    return jsonify({"error": "Journal not found"}), 404

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

