"""
08a - Test Multi-Tool AI Foundry Agent (SQL + AI Search)
Interactive chat with the Foundry Agent that has both SQL and AI Search tools.

Usage:
    python 08a_test_multi_tool_agent.py

Type 'quit' or 'exit' to end the conversation.

This script handles two function tools:
    1. execute_sql - Runs SQL against Fabric Lakehouse via pyodbc
    2. search_documents - Queries Azure AI Search for document content
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
from azure.search.documents import SearchClient

import pyodbc

# ============================================================================
# Configuration
# ============================================================================

# Azure services - from azd environment
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")

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

if not SEARCH_ENDPOINT:
    print("ERROR: AZURE_AI_SEARCH_ENDPOINT not set in .env")
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
        AGENT_ID = agent_ids.get("multi_tool_agent_id")

if not AGENT_ID:
    print("ERROR: No agent ID found.")
    print("       Run 07a_create_foundry_agent.py first or provide --agent-id")
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

# Load Search IDs
search_ids_path = os.path.join(config_dir, "search_ids.json")
if os.path.exists(search_ids_path):
    with open(search_ids_path) as f:
        search_ids = json.load(f)
    INDEX_NAME = search_ids.get("index_name")
else:
    INDEX_NAME = f"{fabric_ids.get('solution_name', 'demo')}-documents"

print(f"\n{'='*60}")
print("Multi-Tool AI Agent Chat")
print(f"{'='*60}")
print("Type 'quit' to exit, 'help' for sample questions\n")

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
if not SQL_ENDPOINT:
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
# AI Search Function
# ============================================================================

def search_documents(query, top=3):
    """Search documents in Azure AI Search"""
    try:
        credential = DefaultAzureCredential()
        search_client = SearchClient(
            endpoint=SEARCH_ENDPOINT,
            index_name=INDEX_NAME,
            credential=credential
        )
        
        # Perform hybrid search (text + vector if available)
        results = search_client.search(
            search_text=query,
            top=min(top, 10),
            query_type="semantic",
            semantic_configuration_name="default-semantic",
            select=["content", "title", "source", "page_number"]
        )
        
        # Format results
        result_lines = []
        for i, result in enumerate(results, 1):
            result_lines.append(f"\n--- Result {i} ---")
            result_lines.append(f"Source: {result.get('source', 'Unknown')} (Page {result.get('page_number', '?')})")
            result_lines.append(f"Title: {result.get('title', 'Unknown')}")
            result_lines.append(f"Content: {result.get('content', '')[:500]}...")
        
        if not result_lines:
            return "No documents found matching the query."
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Search Error: {str(e)}"

# ============================================================================
# Load Sample Questions
# ============================================================================

questions_path = os.path.join(config_dir, "sample_questions.txt")
sample_questions = [
    # Questions that REQUIRE both tools to make sense:
    "What is the total value of orders that would qualify for free shipping based on our shipping policy?",
    "How many of our orders meet the minimum purchase requirement for loyalty rewards?",
    "What's our revenue from product categories that have extended return windows according to our return policy?",
    "Based on our shipping zones, what's the order volume from regions with expedited shipping options?",
]

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

# Get OpenAI client
openai_client = project_client.get_openai_client()

# Create a conversation
conversation = openai_client.conversations.create()
print("-" * 60)

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
            args = json.loads(fc.arguments)
            
            if fc.name == "execute_sql":
                sql_query = args.get("sql_query", "")
                
                print(f"\n  [SQL Tool] Executing query:")
                # Print full query with indentation
                for line in sql_query.strip().split('\n'):
                    print(f"    {line}")
                
                result = execute_sql(sql_query)
                
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result
                })
                
            elif fc.name == "search_documents":
                query = args.get("query", "")
                top = args.get("top", 3)
                
                print(f"\n  [Search Tool] Searching for: {query}...")
                
                result = search_documents(query, top)
                
                # Show the result that goes to the agent
                print(f"  [Search Result]:")
                # Truncate if too long, but show meaningful content
                display = result[:500] if len(result) > 500 else result
                for line in display.strip().split('\n'):
                    print(f"    {line}")
                if len(result) > 500:
                    print(f"    ... ({len(result)} chars total)")
                
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result
                })
            else:
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": f"Unknown function: {fc.name}"
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
        print("\nSample questions (that may use BOTH tools):")
        for q in sample_questions:
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
print("\nGoodbye!")
