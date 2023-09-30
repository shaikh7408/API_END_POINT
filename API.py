from flask import Flask, jsonify, request

app = Flask(_name_)

# Sample data for doctors
doctors = [
    {
        "id": 1,
        "name": "Dr. Smith",
        "specialty": "Cardiologist",
        "available_slots": ["Monday", "Wednesday", "Friday"],
        "max_patients": 10,
    },
    {
        "id": 2,
        "name": "Dr. Johnson",
        "specialty": "Dermatologist",
        "available_slots": ["Tuesday", "Thursday"],
        "max_patients": 8,
    },
]

appointments = []


@app.route("/doctors", methods=["GET"])
def get_doctors():
    return jsonify(doctors)


@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    return jsonify({"message": "Doctor not found"}), 404


@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()
    doctor_id = data.get("doctor_id")
    patient_name = data.get("patient_name")

    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404

    if len(doctor["available_slots"]) == 0:
        return jsonify({"message": "No available slots for this doctor"}), 400

    if len(appointments) >= doctor["max_patients"]:
        return jsonify({"message": "Doctor is fully booked"}), 400

    appointment = {
        "doctor_id": doctor_id,
        "patient_name": patient_name,
        "day": doctor["available_slots"].pop(0),
    }

    appointments.append(appointment)

    return jsonify(appointment), 201


if _name_ == "_main_":
    app.run(debug=True)