import boto3
import json
from helpers.format import format_converse_message

bedrock_runtime = boto3.client('bedrock-runtime')

def converse_stream(client, model_id, system_prompt, prompt, source, inference_config, guardrail_id, guardrail_version):
  guardrail_enabled = True if guardrail_id and guardrail_version else False

  # Setup arguments to send to Bedrock Converse API
  kwargs = {
    "modelId": model_id,
    "inferenceConfig": inference_config,
    "messages": format_converse_message(guardrail_enabled, prompt, source)
  }
  if system_prompt:
    kwargs["system"] = [{ "text": system_prompt }]

  # If Guardrail has been configured, include it in Converse Stream API to evaluate prompt and reponse
  if guardrail_enabled:
    STREAM_PROCESSING_MODE = 'sync' # or 'async'
    guardrail_config = {
      "guardrailIdentifier": guardrail_id, #we can find this on aws bedrock console on safeguards-->guardrails
      "guardrailVersion": guardrail_version,
      "streamProcessingMode": STREAM_PROCESSING_MODE, # processing mode for streaming response
      "trace": "enabled"
    }
    kwargs["guardrailConfig"] = guardrail_config

  # Invoke LLM
  print(kwargs)
  response = bedrock_runtime.converse_stream(**kwargs)

  stream = response.get('stream')
  if stream:
    for event in stream:
      if 'messageStart' in event:
        print(f"Role: {event['messageStart']['role']}")

      if 'contentBlockDelta' in event:
        new_text = event['contentBlockDelta']['delta']['text']
        print(new_text)
        client.send_message(response=new_text, actions="")

      if 'messageStop' in event:
        print(f"Stop reason: {event['messageStop']['stopReason']}")

      if 'metadata' in event:
        metadata = event['metadata']
        if 'trace' in metadata:
          trace = json.dumps(metadata['trace'])
          print("Assessment")
          print(trace)
          client.send_message(response="", actions=trace)

  print("Finished streaming")
  return
