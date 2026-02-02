"""
Build Solution
Master script that runs all steps to build the complete solution.

Usage:
    # Run with AI-generated data (recommended)
    python scripts/00_build_solution.py --ai

    # Run with manual data (Retail demo)
    python scripts/00_build_solution.py

    # Skip specific steps
    python scripts/00_build_solution.py --skip-fabric  # Skip Fabric setup
    python scripts/00_build_solution.py --skip-search  # Skip AI Search upload
    
    # Start from a specific step
    python scripts/00_build_solution.py --from 04

Steps:
    01  - Generate sample data (manual) OR
    01a - Generate sample data (AI-powered, custom industry)
    02  - Setup Fabric workspace (lakehouse, warehouse)
    03  - Load data into Fabric
    04  - Generate NL2SQL prompt
    05  - Create Fabric Data Agent
    06  - Upload documents to AI Search
    07  - Create single-tool Foundry agent (SQL only)
    07a - Create multi-tool Foundry agent (SQL + Search)
    08  - Test single-tool agent
    08a - Test multi-tool agent
"""

import argparse
import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# Configuration
# ============================================================================

STEPS = {
    "01": {"script": "01_generate_sample_data.py", "name": "Generate Sample Data (Manual)", "time": "~10s"},
    "01a": {"script": "01a_generate_sample_data.py", "name": "Generate Sample Data (AI)", "time": "~2min"},
    "02": {"script": "02_setup_fabric.py", "name": "Setup Fabric Workspace", "time": "~30s"},
    "03": {"script": "03_load_fabric_data.py", "name": "Load Data into Fabric", "time": "~1min"},
    "04": {"script": "04_generate_prompt.py", "name": "Generate NL2SQL Prompt", "time": "~5s"},
    "05": {"script": "05_create_fabric_agent.py", "name": "Create Fabric Data Agent", "time": "~30s"},
    "06": {"script": "06_upload_to_search.py", "name": "Upload to AI Search", "time": "~1min"},
    "07": {"script": "07_create_foundry_agent.py", "name": "Create Single-Tool Agent", "time": "~10s"},
    "07a": {"script": "07a_create_foundry_agent.py", "name": "Create Multi-Tool Agent", "time": "~10s"},
    "08": {"script": "08_test_foundry_agent.py", "name": "Test Single-Tool Agent", "time": "interactive"},
    "08a": {"script": "08a_test_multi_tool_agent.py", "name": "Test Multi-Tool Agent", "time": "interactive"},
}

# Default pipeline order
DEFAULT_PIPELINE = ["01", "02", "03", "04", "05", "06", "07a"]
AI_PIPELINE = ["01a", "02", "03", "04", "05", "06", "07a"]

# ============================================================================
# Parse Arguments
# ============================================================================

parser = argparse.ArgumentParser(
    description="End-to-end setup: data → knowledge bases → agents → API → app",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python scripts/00_build_solution.py --ai           # Build with AI-generated data
  python scripts/00_build_solution.py                # Build with manual data
  python scripts/00_build_solution.py --from 04      # Start from step 04
  python scripts/00_build_solution.py --only 07a     # Run only specific steps
  python scripts/00_build_solution.py --skip-fabric  # Skip Fabric steps
"""
)

parser.add_argument("--ai", action="store_true", 
                    help="Use AI-generated data (01a) instead of manual (01)")
parser.add_argument("--industry", type=str, 
                    help="Industry for AI data generation (overrides .env)")
parser.add_argument("--usecase", type=str, 
                    help="Use case for AI data generation (overrides .env)")
parser.add_argument("--size", choices=["small", "medium", "large"],
                    help="Data size for AI generation (overrides .env)")
parser.add_argument("--clean", action="store_true",
                    help="Clean and recreate Fabric artifacts (use when switching scenarios)")

parser.add_argument("--from", dest="from_step", type=str,
                    help="Start from this step (e.g., --from 04)")
parser.add_argument("--only", nargs="+", type=str,
                    help="Run only these steps (e.g., --only 07a 08a)")

parser.add_argument("--skip-fabric", action="store_true",
                    help="Skip Fabric setup steps (02, 03)")
parser.add_argument("--skip-search", action="store_true",
                    help="Skip AI Search upload (06)")
parser.add_argument("--skip-agents", action="store_true",
                    help="Skip agent creation and testing (05, 07, 07a, 08, 08a)")

parser.add_argument("--dry-run", action="store_true",
                    help="Show what would be run without executing")
parser.add_argument("--continue-on-error", action="store_true",
                    help="Continue running steps even if one fails")

args = parser.parse_args()

# ============================================================================
# Determine Pipeline
# ============================================================================

if args.only:
    pipeline = args.only
elif args.ai:
    pipeline = AI_PIPELINE.copy()
else:
    pipeline = DEFAULT_PIPELINE.copy()

# Apply --from filter
if args.from_step:
    try:
        start_idx = pipeline.index(args.from_step)
        pipeline = pipeline[start_idx:]
    except ValueError:
        print(f"ERROR: Step '{args.from_step}' not in pipeline")
        print(f"Available steps: {pipeline}")
        sys.exit(1)

# Apply skip filters
if args.skip_fabric:
    pipeline = [s for s in pipeline if s not in ["02", "03"]]
if args.skip_search:
    pipeline = [s for s in pipeline if s != "06"]
if args.skip_agents:
    pipeline = [s for s in pipeline if s not in ["05", "07", "07a", "08", "08a"]]

# ============================================================================
# Validate
# ============================================================================

# Check all scripts exist
for step in pipeline:
    script_path = os.path.join(script_dir, STEPS[step]["script"])
    if not os.path.exists(script_path):
        print(f"WARNING: Script not found: {STEPS[step]['script']}")

# Load environment from azd + project .env
from load_env import load_all_env
load_all_env()

# AI arguments: CLI > .env
if args.ai and "01a" in pipeline:
    args.industry = args.industry or os.getenv("INDUSTRY")
    args.usecase = args.usecase or os.getenv("USECASE")
    args.size = args.size or os.getenv("DATA_SIZE", "small")
    
    if not args.industry or not args.usecase:
        print("\n" + "="*60)
        print("AI Data Generation Mode")
        print("="*60)
        print("\nNo INDUSTRY/USECASE found in .env or CLI args.")
        print("\nSample scenarios you can use:")
        print("-" * 60)
        print(f"  {'Industry':<18} {'Use Case':<40}")
        print("-" * 60)
        samples = [
            ("Logistics", "Fleet management with delivery tracking"),
            ("Healthcare", "Patient records and appointment scheduling"),
            ("Retail", "Inventory management with sales analytics"),
            ("Finance", "Transaction monitoring and fraud detection"),
            ("Manufacturing", "Production line tracking with quality control"),
            ("Education", "Student enrollment and course management"),
            ("Hospitality", "Hotel reservations and guest services"),
            ("Real Estate", "Property listings and lease management"),
            ("Insurance", "Claims processing and policy management"),
            ("Telecommunications", "Customer service and network monitoring"),
        ]
        for ind, uc in samples:
            print(f"  {ind:<18} {uc:<40}")
        print("-" * 60)
        print()
        if not args.industry:
            args.industry = input("Industry: ").strip()
            if not args.industry:
                print("ERROR: Industry is required. Set INDUSTRY in .env or pass --industry")
                sys.exit(1)
        if not args.usecase:
            args.usecase = input("Use Case: ").strip()
            if not args.usecase:
                print("ERROR: Use case is required. Set USECASE in .env or pass --usecase")
                sys.exit(1)

# ============================================================================
# Print Plan
# ============================================================================

print("\n" + "="*60)
print("Foundry IQ + Fabric IQ Pipeline")
print("="*60)

print(f"\nSteps ({len(pipeline)}):")
for i, step in enumerate(pipeline, 1):
    info = STEPS[step]
    print(f"  {i}. {info['name']} ({info['time']})")

if args.ai and args.industry:
    print(f"\n  Industry: {args.industry}")
    print(f"  Use Case: {args.usecase}")

if args.dry_run:
    print("\n[DRY RUN] No scripts will be executed.")
    sys.exit(0)

print()
input("Press Enter to start...")
print()

# ============================================================================
# Run Pipeline
# ============================================================================

def run_step(step_id):
    """Run a single pipeline step."""
    info = STEPS[step_id]
    script_path = os.path.join(script_dir, info["script"])
    
    print(f"> [{step_id}] {info['name']}...", end=" ", flush=True)
    
    if not os.path.exists(script_path):
        print("SKIP (not found)")
        return True
    
    # Build command
    cmd = [sys.executable, script_path]
    
    # Add arguments for specific scripts
    if step_id == "01a" and args.ai:
        cmd.extend(["--industry", args.industry])
        cmd.extend(["--usecase", args.usecase])
        cmd.extend(["--size", args.size])
    
    # Pass --clean to step 02 if requested
    if step_id == "02" and args.clean:
        cmd.append("--clean")
    
    # Create a clean environment that forces re-reading from .env
    # Remove DATA_FOLDER so child process reads fresh value from .env
    clean_env = os.environ.copy()
    clean_env.pop("DATA_FOLDER", None)
    
    # Run with output captured
    result = subprocess.run(cmd, cwd=os.path.dirname(script_dir), 
                           capture_output=True, text=True, env=clean_env)
    
    if result.returncode != 0:
        print("[FAIL] FAILED")
        print(f"\n  Error output:\n{result.stderr[-500:] if result.stderr else result.stdout[-500:]}")
        return False
    
    print("[OK]")
    return True


# Track results
results = {}
failed = False

for step in pipeline:
    success = run_step(step)
    results[step] = success
    
    if not success:
        failed = True
        if not args.continue_on_error:
            print(f"\nPipeline stopped. Use --continue-on-error to continue despite failures.")
            break

# ============================================================================
# Summary
# ============================================================================

print("\n" + "-"*60)

if failed:
    print("⚠ Pipeline completed with errors")
    sys.exit(1)
else:
    print("[OK] Pipeline completed successfully!")
    print("\nNext: python scripts/08a_test_multi_tool_agent.py")

