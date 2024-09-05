```python
from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

# In-memory storage for simplicity
applicants = {}
applications = {}

@app.route('/apply', methods=['POST'])
def apply_loan():
    data = request.json
    ssn = data['ssn']
    loan_id = str(uuid4())
    
    if ssn not in applicants:
        applicants[ssn] = {'customer_id': str(uuid4()), 'applications': []}
    
    for app_id in applicants[ssn]['applications']:
        if applications[app_id]['status'] == 'active':
            return jsonify({'message': 'Applicant has multiple active loan applications'}), 400
    
    applicants[ssn]['applications'].append(loan_id)
    applications[loan_id] = {'loan_id': loan_id, 'ssn': ssn, 'status': 'active', 'details': data}
    
    return jsonify({'loan_id': loan_id}), 201

@app.route('/applications/<ssn>', methods=['GET'])
def get_applications(ssn):
    if ssn not in applicants:
        return jsonify({'message': 'Applicant not found'}), 404
    
    apps = [applications[app_id] for app_id in applicants[ssn]['applications']]
    return jsonify(apps), 200

@app.route('/application/<loan_id>', methods=['PATCH'])
def manage_application(loan_id):
    if loan_id not in applications:
        return jsonify({'message': 'Application not found'}), 404
    
    data = request.json
    applications[loan_id].update(data)
    
    return jsonify(applications[loan_id]), 200

@app.route('/application/<loan_id>', methods=['POST'])
def submit_application(loan_id):
    if loan_id not in applications:
        return jsonify({'message': 'Application not found'}), 404
    
    if applications[loan_id]['status'] == 'submitted':
        return jsonify({'message': 'Application already submitted'}), 400
    
    applications[loan_id]['status'] = 'submitted'
    return jsonify({'message': 'Application submitted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
```