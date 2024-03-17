# Project README

## Overview

This Python project generates children's book in a PDF format based on predefined themes, spices (elements to add flavor to the story), and topics. 
It also utilizes stable diffusion and prompting techniques to create realistic stories, characters, and images that are consistent and appropriate. This means that some stories may require multiple "passthroughs" with ChatGPT and stable diffusion. 

## Technical Challenges and Approach
To create a polished product, multiple GPT instances are run at once with each one handling a different task as utilizing only one GPT instance rarely creates a well-polished output. In this project, the main GPT instance creates a rough outline of a story with specific character information and theme information fed to it. Another GPT instance is solely responsible for creating the characters which are fed into the main GPT instance. Finally, the third GPT instance is responsible for taking the rough outline of the story and enhancing illustration descriptions with correct character data (from the second GPT instance) which is fed into stable diffusion. The main challenge in this project is creating consistent illustrations. Due to the reliance on LLMs, characters oftentimes change skin colours or start wearing different clothing colours in different illustrations as some illustration prompts are just not specific or worded strangely. This is why a GPT instance was dedicated to only creating prompts for stable diffusion. Finally, stable diffusion sometimes creates unsettling/inappropriate illustrations. To combat this, specific tuning was done to the prompting of the model so that specific keywords received a very negative weighting in the image generation (i.e: scary, text, error, blurry, old, violent, deformed, creepy, low quality, extra limb, realistic).

### Features

### **Customization**:
###### 1. Tones:
- There are a selection of tones that can be incorporated into the story (i.e: Poetic, Mysterious, Fairytale-like, ...).

------------


###### 2. Styles:
- Choose a style of writing from famous authors (i.e: Dr. Seuss, J.K. Rowling, ...)

------------
###### 3. Topics:
- The topic that is focused on throughout the story (i.e: Friendship, Kindness, Family, ...)

------------
###### 4. Themes:
- Themes that are brought into  the story (i.e: Farms, Dragons, Beaches...)

------------
###### 4. Random "Spices":
- Keywords that are thrown into the story generating prompt to create unique and creative stories (i.e: bike, snow, parade, ...)

### **Story Outline Creation**: 
Produces a pdf output of the compiled book with appropriate illustrations. See the sample folder for sample generations. None of the files in this folder have been manually altered in any way and come straight from the program.

### Setup

1. **API Keys**: Ensure you have an OpenAI API key and a Stability AI API key. Set the `openai.api_key` and `api_key` variables in the script with your respective keys. 
2. **Dependencies**: The script requires `openai` Python package.


