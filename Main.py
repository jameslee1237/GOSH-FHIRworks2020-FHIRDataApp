from fhir_parser import FHIR
from flask import Flask, request, jsonify
import requests
import json

r = requests.get("https://localhost:5001/api/Patient/", verify = False)
app = Flask(__name__)
fhir = FHIR()
patients = fhir.get_all_patients()

def extractcomp(observation):
    results = []
    for comp in observation.components:
        subre = []
        subre.append("system: " + comp.system)
        subre.append("code: " + comp.code)
        subre.append("display: " + comp.display)
        if comp.value is not None and comp.unit is not None:
            subre.append("value: " + str(comp.value) + " " + comp.unit)
        if comp.value is not None and comp.unit is None:
            subre.appned("value: " + str(comp.value))
        results.append(str(subre))
    return results

def extractob(observation):
    results = []
    results.append("id: " + observation.uuid)
    results.append("type: " + observation.type)
    results.append("status: " + observation.status)
    results.append("patient_id: " + observation.patient_uuid)
    results.append("encounter_id: " + observation.encounter_uuid)
    results.append("effective_datetime: " + str(observation.effective_datetime))
    results.append("issued_datetime: " + str(observation.issued_datetime))
    return results
    
@app.route("/", methods=['GET'])
def home():
    return '''<h1>GOSH-FHIRworks2020-DataAPI</h1>'''

@app.route("/api/patients", methods=['GET'])
def api_all():
    results = []
    str_id = ""
    for patient in patients:
        str_id = "name" + ": " + patient.name.full_name + ", " + "id" + ": " + patient.uuid
        results.append(str_id)
    return jsonify(results)

@app.route("/api/patient", methods=['GET'])
def api_ind():
    obs = []
    results = []
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id specified"
    for patient in patients:
        if patient.uuid == id:
            obs = fhir.get_patient_observations(id)  
    for o in obs:
        results.append(o.uuid)
    return jsonify(results)

@app.route("/api/observation", methods=['GET'])
def api_indob():
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id specified"
    obser = fhir.get_observation(id)
    info = extractob(obser)
    cinfo = extractcomp(obser)
    final = info + cinfo
    return jsonify(final)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8000, debug = True)
