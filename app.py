from flask import Flask, request, jsonify, json


################ APP ##################

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Powerplant Coding Challenge</h1>
                <p>A flask REST api implementation.</p>'''

@app.route('/productionplan', endpoint='productionplan', methods=['POST'])
def productionplan():
    payload = request.get_json()
    response = power_distribution(payload)
    return jsonify(response)


################ POWER ##################


def grab_payload(path_to_payload):
    with open(path_to_payload, 'r') as file:
        payload = json.loads(file.read())
    return payload

def set_plant_price(payload):
    # Set the price per MWh for each plant in the dict from the json
    for plant in payload["powerplants"]:
        if plant["type"] == "windturbine":
            base_price = 0
        if plant["type"] == "turbojet":
            base_price = payload["fuels"]["kerosine(euro/MWh)"]
        if plant["type"] == "gasfired":
            base_price = payload["fuels"]["gas(euro/MWh)"]
        plant["price"] = base_price / plant["efficiency"]
    return payload
 

def get_merit_order(payload):
    # Get the merit order by sorting the list with all the prices and recovering the indices
    prices = [plant["price"] for plant in payload["powerplants"]]
    argsort = lambda seq: sorted(range(len(seq)), key=seq.__getitem__)
    merit_order = argsort(prices)
    return merit_order

def load_allocation(total_load, payload, merit_order):
    response = []
    load = total_load
    plants = payload["powerplants"]
    for i in merit_order:
        plant = plants[i]
        if load == 0:
            new_plant_dict = {"name": plant["name"], "p": 0}
        # case: pmin is too much for what is remaining
        elif load < plant["pmin"]:
            # Adjust the power from the previous plant used
            response[-1]["p"] += load - plant["pmin"]
            new_plant_dict = {"name": plant["name"], "p": plant["pmin"]}
            load = 0
        # case: pmax is not enough, send full power
        elif load > plant["pmax"]:
            pmax = plant["pmax"]
            if plant["type"] == "windturbine":
                pmax *= payload["fuels"]["wind(%)"] / 100
            new_plant_dict = {"name": plant["name"], "p": round(pmax,1)}
            load -= pmax
        # case: choose remaining power based on the difference
        else:
            new_plant_dict = {"name": plant["name"], "p": round(load,1)}
            load = 0
        response.append(new_plant_dict)
    return response
        

def power_distribution(payload):
    total_load = payload["load"]
    payload = set_plant_price(payload)
    merit_order = get_merit_order(payload)
    response = load_allocation(total_load, payload, merit_order)
    return response


################ MAIN ##################


def main():
    app.run(host="0.0.0.0", port=8888)

if __name__ == '__main__':
    main()