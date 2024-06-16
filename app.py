from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['webhookdb']
collection = db['events']

# Default webpage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.debug(f"Received data: {data}")

    event = None

    # Check for pull request events first as they contain the `pusher` key in the root payload
    if 'pull_request' in data:
        pr_data = data['pull_request']
        event_type = 'merge' if pr_data.get('merged') else 'pull_request'
        event = {
            'type': event_type,
            'author': pr_data['user']['login'],
            'from_branch': pr_data['head']['ref'],
            'to_branch': pr_data['base']['ref'],
            'timestamp': datetime.utcnow()
        }
        if event_type == 'merge':
            event['author'] = pr_data['merged_by']['login']
    
    elif 'pusher' in data:
        event = {
            'type': 'push',
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': datetime.utcnow()
        }
    else:
        return jsonify({'message': 'Unsupported event type'}), 400

    collection.insert_one(event)
    return jsonify({'message': 'Event received'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('timestamp', -1))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)
