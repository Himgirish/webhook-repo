# Github Webhook Trigger Repo
1. Create a python virtual environment using the command `python3 -m venv venv`
2. Activate the virtual environment:
    - On Windows: venv\Scripts\activate
    - On macOS/Linux: source venv/bin/activate
3. Install the required dependencies of the script inside the virtual environment using `pip install -r requirements.txt`
4. Run the script using the command `flask run` -> it wil by default run on http port 5000.
5. I've used ngrok to forward the public request to <https://lobster-cosmic-conversely.ngrok-free.app/> to script running at my `localhost:5000`