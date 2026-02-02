"""
08 - Test AI Foundry Agent with SQL Function
Interactive chat with the Foundry Agent using OpenAI Responses API.

Usage:
    python 08_test_foundry_agent.py

Type 'quit' or 'exit' to end the conversation.

This script handles the execute_sql function calls by:
1. Getting Azure AD token
2. Connecting to Fabric Lakehouse SQL endpoint via pyodbc
3. Executing the query and returning results
"""

import os
import sys
import json
import struct

# Load environment from azd + project .env
from load_env import load_all_env
load_all_env()

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

import pyodbc

# ============================================================================
# Configuration
# ============================================================================

# Azure services - from azd environment
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

# Project settings - from .env
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")
DATA_FOLDER = os.getenv("DATA_FOLDER")

if not ENDPOINT:
    print("ERROR: AZURE_AI_PROJECT_ENDPOINT not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not WORKSPACE_ID:
    print("ERROR: FABRIC_WORKSPACE_ID not set in .env")
    sys.exit(1)

if not DATA_FOLDER:
    print("ERROR: DATA_FOLDER not set in .env")
    print("       Run 01_generate_sample_data.py first")
    sys.exit(1)

data_dir = os.path.abspath(DATA_FOLDER)

# Set up paths for new folder structure
config_dir = os.path.join(data_dir, "config")
if not os.path.exists(config_dir):
    config_dir = data_dir  # Fallback to old structure

# Get agent ID
import argparse
p = argparse.ArgumentParser()
p.add_argument("--agent-id", default=os.getenv("FOUNDRY_AGENT_ID"))
args = p.parse_args()

AGENT_ID = args.agent_id

if not AGENT_ID:
    # Try to load from agent_ids.json
    agent_ids_path = os.path.join(config_dir, "agent_ids.json")
    if os.path.exists(agent_ids_path):
        with open(agent_ids_path) as f:
            agent_ids = json.load(f)
        AGENT_ID = agent_ids.get("foundry_agent_id")

if not AGENT_ID:
    print("ERROR: No agent ID found.")
    print("       Run 07_create_foundry_agent.py first or provide --agent-id")
    sys.exit(1)

# Load Fabric IDs
fabric_ids_path = os.path.join(config_dir, "fabric_ids.json")
if not os.path.exists(fabric_ids_path):
    print("ERROR: fabric_ids.json not found. Run 02_setup_fabric.py first.")
    sys.exit(1)

with open(fabric_ids_path) as f:
    fabric_ids = json.load(f)

LAKEHOUSE_NAME = fabric_ids.get("lakehouse_name")
LAKEHOUSE_ID = fabric_ids.get("lakehouse_id")

print(f"\n{'='*60}")
print("AI Foundry Agent Chat")
print(f"{'='*60}")
print(f"Agent ID: {AGENT_ID}")
print(f"Lakehouse: {LAKEHOUSE_NAME}")
print(f"Type 'quit' to exit, 'help' for sample questions\n")

# ============================================================================
# Get SQL Endpoint
# ============================================================================

def get_sql_endpoint():
    """Get the SQL analytics endpoint for the Lakehouse"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://api.fabric.microsoft.com/.default")
    
    import requests
    headers = {"Authorization": f"Bearer {token.token}"}
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{WORKSPACE_ID}/lakehouses/{LAKEHOUSE_ID}"
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        props = data.get("properties", {})
        sql_props = props.get("sqlEndpointProperties", {})
        return sql_props.get("connectionString")
    return None

SQL_ENDPOINT = get_sql_endpoint()
if SQL_ENDPOINT:
    print(f"SQL Endpoint: {SQL_ENDPOINT}")
else:
    print("WARNING: Could not get SQL endpoint. SQL queries may fail.")

# ============================================================================
# SQL Execution Function
# ============================================================================

def execute_sql(sql_query):
    """Execute SQL query against Fabric Lakehouse and return results"""
    if not SQL_ENDPOINT:
        return "Error: SQL endpoint not available"
    
    try:
        # Get AAD token for SQL
        credential = DefaultAzureCredential()
        token = credential.get_token('https://database.windows.net//.default')
        
        # Build token struct with UTF-16-LE encoding (required for ODBC)
        token_bytes = token.token.encode('UTF-16-LE')
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        
        # Connection string
        conn_str = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SQL_ENDPOINT};Database={LAKEHOUSE_NAME};Encrypt=yes;TrustServerCertificate=no'
        
        # Connect with token
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        conn = pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        # Format results
        result_lines = []
        result_lines.append("| " + " | ".join(columns) + " |")
        result_lines.append("|" + "|".join(["---"] * len(columns)) + "|")
        
        for row in rows[:50]:  # Limit to 50 rows
            values = [str(v) if v is not None else "NULL" for v in row]
            result_lines.append("| " + " | ".join(values) + " |")
        
        if len(rows) > 50:
            result_lines.append(f"\n... and {len(rows) - 50} more rows")
        
        result_lines.append(f"\n({len(rows)} rows returned)")
        
        conn.close()
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"SQL Error: {str(e)}"

# ============================================================================
# Load Sample Questions
# ============================================================================

questions_path = os.path.join(config_dir, "sample_questions.txt")
sample_questions = []
if os.path.exists(questions_path):
    with open(questions_path) as f:
        for line in f:
            if line.strip().startswith("-"):
                sample_questions.append(line.strip()[2:])

# ============================================================================
# Initialize Client
# ============================================================================

credential = DefaultAzureCredential()
project_client = AIProjectClient(
    endpoint=ENDPOINT,
    credential=credential
)

# Get agent details
agent = project_client.agents.get(AGENT_ID)
agent_def = agent.versions['latest']['definition']
MODEL = agent_def['model']
INSTRUCTIONS = agent_def['instructions']
TOOLS = agent_def['tools']

print(f"Model: {MODEL}")

# Get OpenAI client
openai_client = project_client.get_openai_client()

# Create a conversation
conversation = openai_client.conversations.create()
print(f"Conversation ID: {conversation.id}")

# ============================================================================
# Chat Function
# ============================================================================

def chat(user_message):
    """Send a message and handle function calls"""
    
    # Build input with conversation context
    response = openai_client.responses.create(
        model=MODEL,
        input=user_message,
        instructions=INSTRUCTIONS,
        tools=TOOLS,
        conversation={'id': conversation.id}
    )
    
    # Process the response
    final_text = ""
    
    while True:
        # Check for function calls in output
        function_calls = []
        for item in response.output:
            if hasattr(item, 'type'):
                if item.type == 'function_call':
                    function_calls.append(item)
                elif item.type == 'message':
                    # Extract text from message
                    for content in item.content:
                        if hasattr(content, 'text'):
                            final_text += content.text + "\n"
        
        if not function_calls:
            break
        
        # Handle function calls
        tool_outputs = []
        for fc in function_calls:
            if fc.name == "execute_sql":
                args = json.loads(fc.arguments)
                sql_query = args.get("sql_query", "")
                
                print(f"\n  [Executing SQL]")
                print(f"  {sql_query[:100]}{'...' if len(sql_query) > 100 else ''}")
                
                result = execute_sql(sql_query)
                
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result
                })
        
        # Submit function results and continue conversation
        response = openai_client.responses.create(
            model=MODEL,
            input=tool_outputs,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            conversation={'id': conversation.id}
        )
    
    return final_text.strip()

# ============================================================================
# Chat Loop
# ============================================================================

print("-" * 60)

while True:
    try:
        user_input = input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye!")
        break
    
    if not user_input:
        continue
    
    if user_input.lower() in ["quit", "exit", "q"]:
        print("\nGoodbye!")
        break
    
    if user_input.lower() == "help":
        print("\nSample questions:")
        for q in sample_questions[:5]:
            print(f"  - {q}")
        continue
    
    print("\nAgent: ", end="", flush=True)
    
    try:
        response = chat(user_input)
        if response:
            print(response)
        else:
            print("(No response)")
    except Exception as e:
        print(f"Error: {e}")

# Cleanup
print(f"\nSession ended. Conversation ID: {conversation.id}")
