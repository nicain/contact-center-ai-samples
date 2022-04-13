
import os
from google.cloud import dialogflowcx_v3
import uuid
import google.auth
_, project_id = google.auth.default()

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
    agent_split = agent.split('/')

    agent_id = agent_split[5]

    agent_url = f"https://dialogflow.cloud.google.com/cx/projects/{project_id}/locations/global/agents/{agent_id}/flows/00000000-0000-0000-0000-000000000000/flow_creation"

    os.system(f"export AGENT_URL='{agent_url}'")

    print("Restoring Agent")
    sample_restore_agent(agent_name)


def sample_restore_agent(agent_name):
    # Create a client
    client = dialogflowcx_v3.AgentsClient()

    # Initialize request argument(s)
    request = dialogflowcx_v3.RestoreAgentRequest(
        agent_uri="gs://testingeasyagent/travel",
        name=agent_name,
    )

    # Make the request
    operation = client.restore_agent(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)


create_agent()