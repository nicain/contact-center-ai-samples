
import os
import time
from google.cloud import dialogflowcx_v3
import uuid
import google.auth
import json
_, project_id = google.auth.default()
# project_id = "dialogflow-cx-demo-1-348717"

from flask import Flask, render_template

app = Flask(__name__)

from set_session_param_sample import SetSessionParamSample

with open('/import/WEBHOOK_URI', 'r') as file_handle:
    webhook_uri = file_handle.read().strip()

if os.environ.get('ENV', 'prod') == 'prod':
    sample = SetSessionParamSample(
        use_implicit_credentials=True,
        project_id=project_id,
        agent_display_name=f'sample-agent-{int(time.time())}',
        webhook_uri=webhook_uri,
    )
    sample.setup()
    _AGENT_LOC = sample.start_flow_delegator.flow.name
    _WEBHOOK_LOC = sample.webhook_delegator.webhook.generic_web_service.uri.split('/')[-1]
    _PROJECT_ID = sample.project_id
    _AGENT_NAME = '/'.join(_AGENT_LOC.split('/')[:-2])
else:
    _AGENT_LOC = 'FOO'
    _WEBHOOK_LOC = 'BAR'
    _PROJECT_ID = 'BAZ'
    _AGENT_NAME = 'BOC'

@app.route('/')
def index():
    # agent_url = f"https://dialogflow.cloud.google.com/cx/{sample.start_flow_delegator.flow.name}"
    # webhook_url = f"https://console.cloud.google.com/functions/details/us-central1/{sample.webhook_delegator.webhook.generic_web_service.uri.split('/')[-1]}?project={sample.project_id}"
    agent_url = f"https://dialogflow.cloud.google.com/cx/{_AGENT_LOC}"
    webhook_url = f"https://console.cloud.google.com/functions/details/us-central1/{_WEBHOOK_LOC}?project={_PROJECT_ID}"
    agent_id = agent_url.split('/')[-3]
    return render_template(
        'index.html', 
        agent_url=agent_url, 
        webhook_url=webhook_url, 
        agent_id=agent_id, 
        project_id=_PROJECT_ID,
        agent_name=_AGENT_NAME)

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

    print("Restoring Agent")
    import_agent(agent_name)


def import_agent(agent_name):

    # Gets agent uri 
    with open('agent_uri.json','r') as f:
        loaded_json = json.loads(f.read())

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

# create_agent()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)