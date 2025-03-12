import boto3
from helpers.format import format_converse_message

bedrock_runtime = boto3.client('bedrock-runtime')

def apply(client, model_id, system_prompt, prompt, source, inference_config, guardrail_id, guardrail_version):
  guardrail_enabled = True if guardrail_id and guardrail_version else False

  # Setup arguments to send to Bedrock Converse API
  kwargs = {
    "modelId": model_id,
    "inferenceConfig": inference_config,
    "messages": format_converse_message(guardrail_enabled, prompt, source)
  }
  if system_prompt:
    kwargs["system"] = [{ "text": system_prompt }]

  # STEP 1
  # Evaluate input with Guardrail (if enabled)
  if guardrail_enabled:
    content = [{"text": {"text": prompt}}]

    # Evaluate input
    print("Evaluating input")
    response = bedrock_runtime.apply_guardrail(
      guardrailIdentifier=guardrail_id,
      guardrailVersion=guardrail_version,
      source='INPUT',  # or 'OUTPUT' depending on your use case
      content=content
    )
    print(response)

    if response['action'] == 'GUARDRAIL_INTERVENED':
      output_text = ""
      for output in response['outputs']:
        output_text += output["text"]

      output_assessments = response['assessments']
      print("Guardrail intervened.")
      # Break code execution, no need to invoke LLM. Send the Guardrails message and assessment to client
      client.send_message(output_text, output_assessments)
      
      return
    else:
      print("Guardrail did not intervene.")
    
  # STEP 2
  # Inference LLM with Converse API without attaching Guardrail
  print("Getting output from LLM")
  print(kwargs)
  response = bedrock_runtime.converse(**kwargs)
  print(response)
  
  # STEP 3
  # Evaluate the response with Guardrail (if enabled)
  output_message = response["output"]["message"]

  if guardrail_enabled:
    content = output_message["content"]
    content = [{"text": {"text": item["text"]}} for item in content] # Format needed for apply API
    
    # Evaluate output
    print("Evaluating output")
    response = bedrock_runtime.apply_guardrail(
      guardrailIdentifier=guardrail_id,
      guardrailVersion=guardrail_version,
      source='OUTPUT',  # or 'INPUT' depending on your use case
      content=content
    )
    print(response)

    # If Guardrails intervene, use output message from Guardrails, otherwise use LLM response
    output_text = ""
    output_assessments = ""
    
    if response["action"] == "GUARDRAIL_INTERVENED":
      for output in response['outputs']:
        output_text += output["text"]

      output_assessments = response['assessments']
      print("Guardrail intervened.")
    else:
      for content in output_message["content"]:
        output_text += content["text"]
      print("Guardrail did not intervene.")
    client.send_message(output_text, output_assessments)
    
    return
  else:
    # Guardrail not enabled, send LLM response directly to client
    output_text = ""
    for content in output_message["content"]:
      output_text += content["text"]
    client.send_message(output_text, "")
    return
