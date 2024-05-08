from flask import Flask, jsonify
import requests

app = Flask(__name__)
app_name = "pollquest-question-service"
@app.route('/'+app_name+'/api/question/<question-id>', methods=['GET'])
def get_question(question_id):
    response = requests.get("https://api.example.com/data", params={"question_id": question_id})
    if response.status_code == 200:
            return jsonify({
                'question_id': question_id,
                'question': questions_data[question_id],
                'external_data': response.json()
            })
    else:
            return jsonify({'error': 'Failed to fetch external data'}), response.status_code
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
