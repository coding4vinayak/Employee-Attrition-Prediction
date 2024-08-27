from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load the pre-trained model and label encoders
model_path = os.path.join('app', 'models', 'attrition_model.pkl')
encoders_path = os.path.join('app', 'models', 'label_encoders.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(encoders_path, 'rb') as f:
    label_encoders = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Check if the request contains JSON data
            if request.is_json:
                data = request.json
            else:
                # Extract form data if JSON is not provided
                data = request.form.to_dict()

            # Convert to DataFrame
            input_df = pd.DataFrame([data])

            # Encode categorical variables
            for column, le in label_encoders.items():
                if column in input_df:
                    input_df[column] = le.transform(input_df[column])

            # Predict using the model
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1]

            # Return the result as JSON
            result = {
                'prediction': 'Attrition' if prediction == 1 else 'No Attrition',
                'probability': probability
            }
            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
