# auto_comp
Simple interface to query a PACS server and obtain a list of relevant comparison studies using Mistral.

# Cloning the repository
git clone https://github.com/apyrros/auto_comp

# Install ollama (https://ollama.ai/)
'curl https://ollama.ai/install.sh | sh'
'ollama run mistral'

# Usage
# api_server.py
The api_server.py script utilizes the Flask web framework to run a lightweight server capable of handling API calls. It's designed to listen for requests, process them according to the defined routes and methods, and return responses.  

# query_pacs.py
Thos script is designed to automate the process of querying a PACS server for a list of studies for a given MRN. Once the list of studies is reterieved mistral sorts and formats the data according to the provided study description. 

# compare-llm.ahk
The compare-llm.ahk script is a specialized tool designed to interface with PowerScribe 360. Its primary function is to automate the workflow as follows:
Search MRN Number and Study Description: The script searches the PowerScribe 360 sidebar for a MRN and study description. 
Sending Information: Once the accession number is located it sends it to the server, effectively initiating the process.
The script is started by pressing Windows Key + F1. You will need to download autohotkey v1.1 (https://www.autohotkey.com/download/).

# License
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License. This license allows reusers to copy and redistribute the material in any medium or format and remix, transform, and build upon the material, as long as attribution is given to the creator. The license allows for non-commercial use only, and otherwise maintains the same freedoms as the regular CC license.

This software, "Auto RadReport," is provided as a prototype and for informational purposes only. It is not necessarily secure or accurate and is provided "as is" without warranty of any kind. Users should use this software at their own risk.

We make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the software or the information, products, services, or related graphics contained on the software for any purpose. Any reliance you place on such information is therefore strictly at your own risk.

This software is not intended for use in medical diagnosis or treatment or in any activity where failure or inaccuracy of use might result in harm or loss. Users are advised that health treatment or diagnosis decisions should only be made by certified medical professionals.
