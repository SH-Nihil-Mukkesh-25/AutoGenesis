#!/usr/bin/env python3
"""
Autogenesis CLI - Cline-compatible autonomous coding agent.
Usage: python autogenesis.py "Build a calculator"
"""
import argparse
import sys
import os
import json

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def main():
    parser = argparse.ArgumentParser(
        prog='autogenesis',
        description='Autonomous AI Coding Agent - Plans, codes, tests, and deploys'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen = subparsers.add_parser('generate', help='Generate a new project')
    gen.add_argument('idea', type=str, help='Project description')
    gen.add_argument('--output', '-o', type=str, default='./output', help='Output directory')
    
    # Fix command
    fix = subparsers.add_parser('fix', help='Auto-fix bugs in code')
    fix.add_argument('file', type=str, help='File to fix')
    fix.add_argument('--error', '-e', type=str, help='Error message')
    
    # Test command
    test = subparsers.add_parser('test', help='Generate tests for code')
    test.add_argument('file', type=str, help='File to generate tests for')
    
    # Stats command
    subparsers.add_parser('stats', help='Show AI learning stats')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        print(f"🚀 Autogenesis: Generating project...")
        print(f"   Idea: {args.idea}")
        print(f"   Output: {args.output}")
        
        try:
            from agent.orchestrator import run_pipeline
            result = run_pipeline(args.idea)
            
            print(f"\n✅ Generated {len(result['code_files'])} files:")
            for f in result['code_files']:
                print(f"   - {f}")
            print(f"\n📊 XP Gained: +{result.get('xp_gained', 0)}")
            print(f"🧠 AI Level: {result['intelligence']['level']}%")
            
        except ImportError:
            print("⚠️  Running in demo mode (backend not available)")
            print("   Generated: main.py, test_main.py, Dockerfile, .github/workflows/main.yml")
    
    elif args.command == 'fix':
        print(f"🔧 Auto-fixing: {args.file}")
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            
            from agent.capabilities import auto_fix_code
            result = auto_fix_code(code, args.error or "Fix any bugs")
            
            with open(args.file, 'w') as f:
                f.write(result['fixed_code'])
            
            print(f"✅ Fixed and saved: {args.file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif args.command == 'test':
        print(f"🧪 Generating tests for: {args.file}")
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            
            from agent.capabilities import generate_unit_tests
            result = generate_unit_tests(code, args.file)
            
            test_file = result['path']
            with open(test_file, 'w') as f:
                f.write(result['content'])
            
            print(f"✅ Tests saved: {test_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif args.command == 'stats':
        print("📊 Autogenesis AI Stats")
        print("-" * 30)
        try:
            from agent.intelligence import get_intelligence
            intel = get_intelligence()
            
            print(f"   Stage: {intel['stage_emoji']} {intel['stage_name']}")
            print(f"   Level: {intel['level']}%")
            print(f"   XP: {intel['xp']}")
            print(f"   Projects: {intel['total_projects']}")
            print(f"   Files: {intel['total_files']}")
            print(f"   Languages: {', '.join(intel['languages']) or 'None'}")
            
        except:
            print("   No stats available yet. Generate a project first!")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
