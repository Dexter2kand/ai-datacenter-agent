# AI Data Center Troubleshooting Agent

An AI-powered maintenance knowledge and troubleshooting assistant for data center infrastructure, built with Python, Streamlit, SQLite, and Ollama.

## Overview

This project demonstrates how local Large Language Models (LLMs) can support technical fault analysis by retrieving historical maintenance incidents and generating contextual troubleshooting recommendations.

The application is designed as a prototype for data center equipment maintenance and incident knowledge management.

## Features

- **Equipment Registry:** Register and view UPS, PDU, generators, cooling equipment, servers, and other infrastructure.
- **Incident Management:** Record alarms, symptoms, root causes, corrective actions, contractors, and verification status.
- **AI Troubleshooting:** Analyze new fault descriptions using historical maintenance records.
- **Incident Retrieval:** Find potentially similar incidents using keyword matching.
- **Maintenance Dashboard:** Monitor equipment counts, recorded incidents, and verified repairs.
- **Local AI Processing:** Generate troubleshooting explanations using Ollama without relying on a cloud LLM API.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web dashboard |
| SQLite | Equipment and incident database |
| Ollama | Local LLM inference |
| LangChain | LLM integration |
| Pandas | Data visualization and tables |
| Qwen2.5 3B | Local language model |

## Project Structure

```text
DataCenter_AI/
├── app.py
├── ai_agent.py
├── database.py
└── .gitignore
```

The SQLite database is created locally and excluded from Git.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Dexter2kand/ai-datacenter-agent.git
cd ai-datacenter-agent
```

**2. Create a Python virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install streamlit pandas langchain langchain-ollama
```

**4. Install Ollama and download the model**

```bash
ollama pull qwen2.5:3b
```

Ensure the Ollama service is running.

**5. Start the application**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Example Use Case

A UPS reports:

**Alarm:** FAN_FAILURE

**Symptoms:** High temperature and unusual fan noise.

The AI assistant searches historical incidents and identifies relevant maintenance records.

It can then provide:

1. Similar historical incidents and their IDs
2. Possible causes based on available evidence
3. Suggested diagnostic checks
4. Limitations and uncertainty

The system distinguishes historical evidence from AI-generated hypotheses.

## Current Limitations

- Similarity retrieval uses keyword matching, not semantic vector search.
- AI responses require human verification.
- Equipment data and incident reports must be entered manually.
- This prototype is not connected to live DCIM/BMS monitoring systems.
- The application is not designed to autonomously control equipment.

**Safety:** Troubleshooting suggestions are informational only. Maintenance of UPS and other critical electrical infrastructure must follow manufacturer procedures and site safety requirements and be performed by authorized personnel.

## Planned Improvements

- PDF maintenance report upload and text extraction
- Retrieval-Augmented Generation (RAG) with semantic search
- Source references to maintenance documents
- Automated PDF incident reports
- Integration with monitoring and alarm data
- Expanded equipment history and analytics

## Author

**Ali Sheikholeslamikandelosi**

Electronic Engineering | Automotive Diagnostics | Python & AI Development

GitHub: https://github.com/Dexter2kand

## Project Status

Functional prototype — under active development.
