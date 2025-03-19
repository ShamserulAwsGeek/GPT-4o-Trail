import json
from inference.converse import converse
from inference.apply import apply
from inference.converse_stream import converse_stream
from helpers.client import WebsocketClient

MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
MAX_TOKENS = 2048
TEMPERATURE = 0

# Enable Guardrail
guardrail_id = "" # replace with your own Guardrail ID
guardrail_version = "" # Replace with a version number (as string) if you have published versions of your Guardrail

def lambda_handler(event, context):
  print(event)

  connection_id = event.get("requestContext", {}).get("connectionId")
  domain = event.get("requestContext", {}).get("domainName")
  stage = event.get("requestContext", {}).get("stage")
  api_endpoint = f"https://{domain}/{stage}"
  client = WebsocketClient(api_endpoint=api_endpoint, connection_id=connection_id)

  body = json.loads(event["body"])
  system_prompt = body["system_prompt"]
  prompt = body["prompt"]
  source = body["source"]
  guardrail_mode = body["guardrail_mode"]

  inference_config = {
    "temperature": TEMPERATURE,
    "maxTokens": MAX_TOKENS
  }
#try & catch attribute is added to make sure to parse the request so that it does not break or stop in between during any actions!
  try:
    if guardrail_mode == 'stream':
      converse_stream(
        client=client,
        model_id=MODEL_ID,
        system_prompt=system_prompt,
        prompt=prompt,
        source=source,
        inference_config=inference_config,
        guardrail_id=guardrail_id,
        guardrail_version=guardrail_version
      )
    elif guardrail_mode == 'apply':
      apply(
        client=client,
        model_id=MODEL_ID,
        system_prompt=system_prompt,
        prompt=prompt,
        source=source,
        inference_config=inference_config,
        guardrail_id=guardrail_id,
        guardrail_version=guardrail_version
      )
    else:
      converse(
        client=client,
        model_id=MODEL_ID,
        system_prompt=system_prompt,
        prompt=prompt,
        source=source,
        inference_config=inference_config,
        guardrail_id=guardrail_id,
        guardrail_version=guardrail_version
      )

  except Exception as e: 
    print("Error happened")
    print(e)
  else:
    print("request completed")

  return {
      "statusCode": 200,
      "body": "Success"
  }
