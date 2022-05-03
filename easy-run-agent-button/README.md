# Dialogflow Agent Import Button

If you have a public repository, you can add this button to your `README.md` and copy the deploy folder and 
let anyone import your agent into thier [Dialogflow CX](https://dialogflow.cloud.google.com/cx) project 
with a single click. 

[![Import Dialogflow Agent](./resources/button.svg)](https://deploy.cloud.run)

### Add the Import Dialogflow Agent Button to Your Repo

1. Copy & paste this markdown:

    ```text
    [![Import Dialogflow Agent](./resources/button.svg)](https://deploy.cloud.run)
    ```

1. Copy the Dockerfile, app.json and the import folder over to your own repo. 
The import folder and files will allow the cloud run instance to import the agent into your project.

1. Change the agent uri to the GCS location where you store the agent you want to import


### Using the Import Dialogflow Agent Button

1. Click the button to import the agent

1. Authorize the cloud shell to make GCP API calls 
 
1. Select the project Dialogflow CX is enabled on 

1. Select the location

1. Now the import should be running depending on  the size of the agent it might take a couple minutes to import your agent

1. Now you can test and use your agent! 

### Notes

- Disclaimer: This is not an officially supported Google product.
- See [LICENSE](./LICENSE) for the licensing information.
