"""
CLI entry point for PRA COREP Reporting Assistant.
"""
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import CorepPipeline
from reporting import ReportGenerator


# Default example question
DEFAULT_QUESTION = (
    "How should a UK bank report its Common Equity Tier 1 capital "
    "under PRA COREP Own Funds?"
)


def main():
    """Main entry point."""
    # Get question from command line or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = DEFAULT_QUESTION
    
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     PRA COREP REPORTING ASSISTANT - PROTOTYPE v0.1          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Initialize and run pipeline
        pipeline = CorepPipeline()
        output = pipeline.run(question)
        
        # Generate and print full report
        report = ReportGenerator.generate_full_report(output)
        print(report)
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nMake sure OPENAI_API_KEY environment variable is set.")
        sys.exit(1)


if __name__ == "__main__":
    main()
