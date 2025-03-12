# Helper method to format content block within the message
def format_converse_message(guardrail_enabled, prompt, source):
  if not source:
    messages = [{
      "role": "user",
      "content": [{ "text": prompt }]
    }]
  
  else:
    if not guardrail_enabled:
      messages = [{
        "role": "user",
        "content": [{ "text": source }, { "text": prompt }]
      }]

    else:
      messages = [{
        "role": "user",
        "content": [
          {
            "guardContent": {
              "text": {
                "text": source,
                "qualifiers": ["grounding_source"]
              }
            }
          },
          {
            "guardContent": {
              "text": {
                "text": prompt,
                "qualifiers": ["query"]
              }
            }
          }
        ]
      }]
  
  return messages
