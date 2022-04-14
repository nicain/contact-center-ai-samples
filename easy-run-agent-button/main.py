
import os
from google.cloud import dialogflowcx_v3
import uuid
import google.auth
_, project_id = google.auth.default()

from flask import Flask

app = Flask(__name__)

client = dialogflowcx_v3.AgentsClient()

@app.route('/')
def index():
    return 'Web App with Python Flask!'

def create_agent():

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

    print("Restoring Agent")
    sample_restore_agent(agent_name)


def sample_restore_agent(agent_name):

    # Initialize request argument(s)
    request = dialogflowcx_v3.RestoreAgentRequest(
        agent_uri="gs://testingeasyagent/travel",
        name=agent_name,
        restore_option="KEEP"
    )

    # Make the request
    client.restore_agent(request=request)


create_agent()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)