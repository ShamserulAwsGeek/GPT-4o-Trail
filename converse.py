import boto3
from helpers.format import format_converse_message

bedrock_runtime = boto3.client('bedrock-runtime')

def converse(client, model_id, system_prompt, prompt, source, inference_config, guardrail_id, guardrail_version):
  guardrail_enabled = True if guardrail_id and guardrail_version else False

  # Setup arguments to send to Bedrock Converse API
  kwargs = {
    "modelId": model_id,
    "inferenceConfig": inference_config,
    "messages": format_converse_message(guardrail_enabled, prompt, source)
  }
  if system_prompt:
    kwargs["system"] = [{ "text": system_prompt }]

  # If Guardrail has been configured, include it in Converse API to evaluate prompt and reponse
  if guardrail_enabled:
    guardrail_config = {
      "guardrailIdentifier": guardrail_id,
      "guardrailVersion": guardrail_version,
      "trace": "enabled"
    }
    kwargs["guardrailConfig"] = guardrail_config

  # Invoke LLM
  print(kwargs)
  response = bedrock_runtime.converse(**kwargs)
  print(response)

  # If Guardrails intervene, output message will come from Guardrails, otherwise it will be LLM invocation results
  output_message = response["output"]["message"]
  output_text = ""
  for content in output_message["content"]:
    output_text += content["text"]

  # If Guardrails tracing is enabled, evaluation result will be available
  output_trace = {}
  if "trace" in response:
    output_trace = response["trace"]
    
  client.send_message(output_text, output_trace)
  return
