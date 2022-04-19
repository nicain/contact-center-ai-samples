
import os
from google.cloud import dialogflowcx_v3
import uuid
import google.auth
import json
_, project_id = google.auth.default()

from flask import Flask

app = Flask(__name__)

json_file = open("agent_uri.json","r")
loaded_json = json.loads(json_file)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

def create_agent():
    client = dialogflowcx_v3.AgentsClient()

    location = "global"

    agent = dialogflowcx_v3.Agent(
        display_name="sample-agent-" + str(uuid.uuid1()),
        default_language_code="en",
        time_zone="America/Los_Angeles",
    )

    request = dialogflowcx_v3.CreateAgentRequest(
        parent=f"projects/{project_id}/locations/{location}",
        agent=agent,)

    print("Creating Agent")

    created_agent = client.create_agent(request=request)
    agent_name = created_agent.name

    print(loaded_json["agent_uri"])

    print("Restoring Agent")
    sample_restore_agent(agent_name)


def sample_restore_agent(agent_name):
    # Create a client
    client = dialogflowcx_v3.AgentsClient()

    # Initialize request argument(s)
    request = dialogflowcx_v3.RestoreAgentRequest(
        agent_uri=loaded_json["agent_uri"],
        name=agent_name,
    )

    # Make the request
    operation = client.restore_agent(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)


create_agent()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)