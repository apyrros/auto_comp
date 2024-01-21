from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    # Extract MRN and study type from the request
    data = request.json
    mrn = data.get('mrn')
    study_type = data.get('study_type')

    if not mrn or not study_type:
        return "MRN and study type are required.", 400

    # Call another script and pass the MRN and study type
    # Make sure to provide the correct path to your script
    # Running the script with the MRN and study type, and capturing the output
    result = subprocess.run(["python", "query_pacs.py", mrn, study_type], capture_output=True, text=True)

    # Return the standard output along with the message
    return f"Query initiated for MRN: {mrn} and Study Type: {study_type}\nOutput: {result.stdout}"

if __name__ == '__main__':
    # Run the app on a specific IP and port
    app.run(host='127.0.0.1', port=6990, debug=True)
