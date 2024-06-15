from flask import Flask, request, jsonify
import util
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        logging.error(f"Error in /get_location_names: {str(e)}")
        response = jsonify({'error': 'An error occurred while fetching location names.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        if not request.form:
            logging.error("No form data received")
            response = jsonify({'error': 'Invalid input. Please provide all required fields.'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        data = request.form
        logging.info(f"Received data: {data}")

        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        if total_sqft <= 0 or not location or bhk <= 0 or bath <= 0:
            logging.error("Invalid input values")
            response = jsonify({'error': 'Invalid input values. Please check your data.'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except KeyError as e:
        logging.error(f"Missing data in request: {str(e)}")
        response = jsonify({'error': 'Invalid input. Please provide all required fields.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400
    except ValueError as e:
        logging.error(f"Invalid data format: {str(e)}")
        response = jsonify({'error': 'Invalid input format. Please check your data.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400
    except Exception as e:
        logging.error(f"Error in /predict_home_price: {str(e)}")
        response = jsonify({'error': 'An error occurred while predicting home price.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

if __name__ == '__main__':
    util.load_saved_artifacts()
    app.run(debug=True)
