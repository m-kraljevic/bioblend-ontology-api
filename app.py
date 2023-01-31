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

# Get the ids of the sample history, GO files, sample annotation file and sample study file
sample_history_id = ""
ontology_ids = []
sample_annotation_id = ""
sample_study_id = ""

# Iterate over the list of histories
for history in histories:
    # I am only interested in the sample history I created in Galaxy for this demo
    if history['name'] == 'Sample history':
        # Get a list of datasets in the history
        datasets = gi.histories.show_history(history['id'], contents=True)
        sample_history_id = history['id']
        # Iterate over the list of datasets
        for dataset in datasets:
            if dataset['name'] == 'Sample annotation':
                sample_annotation_id = dataset['id']
            if dataset['name'] == 'Sample study':
                sample_study_id = dataset['id']
            if dataset['extension'] == 'obo' or dataset['extension'] == 'owl':
                ontology_ids.append(dataset['id'])


# Define the input data for the job
inputs = {
  'go':{'src': 'hda', 'id': ontology_ids[1]},
  'annotation':{'src': 'hda', 'id': sample_annotation_id},
  'study':{'src': 'hda', 'id': sample_study_id}
}

# Run the job
go_enrichment_tool_id = gi.tools.get_tools(name='GOEnrichment')[0]['id']
toolShow = toolClient.show_tool(go_enrichment_tool_id, io_details=True)
results = gi.tools.run_tool(history_id=sample_history_id, tool_id=go_enrichment_tool_id, tool_inputs=inputs)

# Get the ID of the GOEnrichment tool
@app.route('/', methods=['GET'])
def hello_world():
    message = [sample_history_id, sample_annotation_id, sample_study_id, ontology_ids[1]]
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True) 