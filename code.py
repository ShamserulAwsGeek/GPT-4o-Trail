"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Gothic architecture, which flourished from the late 12th to the 16th century, is characterized by several distinctive features:

1. **Pointed Arches**: A hallmark of Gothic architecture, these arches distribute weight more evenly, allowing for taller and more slender structures.

2. **Ribbed Vaults**: These are intersecting ribbed arches used to support the roof, facilitating the construction of complex ceiling designs and enabling higher ceilings.

3. **Flying Buttresses**: Exterior supports that transfer the weight of the roof and walls outward, allowing for thinner walls and larger windows.

4. **Large Stained Glass Windows**: Often featuring intricate designs and biblical scenes, these windows allowed more light into the structures and contributed to the ethereal atmosphere.

5. **Ornate Decoration**: This includes detailed stone carvings, sculptures, and tracery, often depicting religious themes or fantastical creatures like gargoyles.

6. **Vertical Emphasis**: Structures are designed to draw the eye upward, creating a sense of height and grandeur.

7. **Spire and Towers**: Tall, ornate spires and towers were used to create dramatic silhouettes and enhance the verticality of the buildings.

8. **Elaborate Facades**: Frontages are typically richly decorated with sculptures, reliefs, and intricate stonework.

These elements helped create the dramatic and awe-inspiring structures typical of Gothic cathedrals and other buildings.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
            "content": "Why France  is so famous?"
            "content": "When is the best time to visit France?"
        }
    ],
    model="gpt-4o",
    temperature=0.4,
    max_tokens=2350,
    top_p=1
)

print(response.choices[0].message.content)



import os
from openai import OpenAI

# Fetch configuration from environment variables
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")
API_KEY = os.environ.get("GITHUB_TOKEN")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")

if not API_KEY:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """Gothic architecture, which flourished from the late 12th to the 16th century, is characterized by several distinctive features:

1. **Pointed Arches**: A hallmark of Gothic architecture, these arches distribute weight more evenly, allowing for taller and more slender structures.

2. **Ribbed Vaults**: These are intersecting ribbed arches used to support the roof, facilitating the construction of complex ceiling designs and enabling higher ceilings.

3. **Flying Buttresses**: Exterior supports that transfer the weight of the roof and walls outward, allowing for thinner walls and larger windows.

4. **Large Stained Glass Windows**: Often featuring intricate designs and biblical scenes, these windows allowed more light into the structures and contributed to the ethereal atmosphere.

5. **Ornate Decoration**: This includes detailed stone carvings, sculptures, and tracery, often depicting religious themes or fantastical creatures like gargoyles.

6. **Vertical Emphasis**: Structures are designed to draw the eye upward, creating a sense of height and grandeur.

7. **Spire and Towers**: Tall, ornate spires and towers were used to create dramatic silhouettes and enhance the verticality of the buildings.

8. **Elaborate Facades**: Frontages are typically richly decorated with sculptures, reliefs, and intricate stonework.

These elements helped create the dramatic and awe-inspiring structures typical of Gothic cathedrals and other buildings."""
        },
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "user", "content": "Why is France so famous?"},
        {"role": "user", "content": "When is the best time to visit France?"}
    ],
    model=MODEL,
    temperature=0.4,
    max_tokens=2350,
    top_p=1
)

print(response.choices[0].message.content)
