# GUIDE: LLM-Driven GUI Generation Decomposition for Automated Prototyping

[![DOI](https://zenodo.org/badge/870925443.svg)](https://doi.org/10.5281/zenodo.13918826)

The supplementary material of our submission to the ICSE 2025 conference demonstration track is structured as follows:

- **datasets**: This directory contains the datasets employed in our approach including the created *Material Design* component library, the configuration mappings of *Material Design* GUI components to specific configurations, the complete *Material Design* component library specifcation, GUI descriptions for the evaluation and the respective evaluation results from the conducted user on Prolific
- **evaluation**: This directory contains the script used to compute the main evaluation results and statistical tests
- **plugin**: Source code and all additional resources for the *Figma* plugin inclduing a detailed installation guide to run the *Figma* plugin
- **quartapp**: This directory contains our Python-based backend in the form of a quartapp including *(1)* the code for user authentification on the served REST API, *(2)* the code for evaluation of the efficiency improvements comparing standard prompting with a RAG-based approach, *(3)* the code and prompts generate the GUI feature collections based on high-level GUI descriptions, *(4)* the code and prompts for generating the *Material Design* GUI feature implementations, *(5)* the code for testing the different methods, *(6)* the code for utilities, *(7)* the code for configuration of *OpenAI* and employed logger, *(8)* the main quart app serving the REST API and *(9)* a detailed installation guide
- **scripts**:  Bash scripts for deploying the backend on a server using *gunicorn*

<img src="https://github.com/GUIDE-Prototyper/GUIDE/blob/main/datasets/images/GUIDE_architecture_overview_updated.png?raw=true" width="100%">

# License Notice 
This repository contains multiple components with different licenses. Below is a breakdown of the applicable licenses for each part: 
- **Top-Level Repository (Apache 2.0)**: Unless otherwise noted, all files in this repository are licensed under the **Apache License 2.0**.  See the [LICENSE](./LICENSE) file for more details. 
- **Figma Plugin (MIT License)**: The Figma plugin located in the `plugin/` directory is licensed under the **MIT License**.  See [`plugin/LICENSE`](./plugin/LICENSE) for details. 
