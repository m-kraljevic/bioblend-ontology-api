from flask import Flask, jsonify
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.tools import ToolClient
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
api_key = os.getenv("API_KEY")
galaxy_url = os.getenv("GALAXY_URL")
gi = GalaxyInstance(url=galaxy_url, key=api_key)
toolClient = ToolClient(gi)

histories = gi.histories.get_histories(all=True)
obo_files = []
txt_files = []
all_files = []

# Iterate over the list of histories
for history in histories:
    # Get a list of datasets in the history
    datasets = gi.histories.show_history(history['id'], contents=True)
    # Iterate over the list of datasets
    for dataset in datasets:
        # Check if the dataset is an .obo file
        if dataset['extension'] == 'obo':
            obo_files.append({'history':history['id'],'name':dataset['name'],'id':dataset['id']})
        if dataset['extension'] == 'tab':
            txt_files.append({'history':history['id'],'name':dataset['name'],'id':dataset['id']})
        all_files.append({'history':history['id'],'name':dataset['name'],'id':dataset['id']})


# Define the input data for the job{
inputs = {
  'go':{'src': 'hda', 'id': "f158df71bb77bb86"},
  'annotation':{'src': 'hda', 'id': "9752b387803d3e1e"},
  'study':{'src': 'hda', 'id': "5a9381f02a7b89af"}
}

# Run the job
go_enrichment_tool_id = gi.tools.get_tools(name='GOEnrichment')[0]['id']
toolShow = toolClient.show_tool(go_enrichment_tool_id, io_details=True)
inputParams = toolShow['inputs']
gi.tools.run_tool(history_id='f597429621d6eb2b', tool_id=go_enrichment_tool_id, tool_inputs=inputs)

# Get the ID of the GOEnrichment tool
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": all_files})

if __name__ == '__main__':
    app.run(debug=True) 