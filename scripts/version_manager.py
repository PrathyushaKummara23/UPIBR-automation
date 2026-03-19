#!/usr/bin/env python3
import argparse
import os
import sys

def generate_experimental_version(baseline_version):
    """
    Convert baseline version to experimental version
    8 -> F, 000 -> 121 (increment logic)
    """
    if not baseline_version.startswith('8'):
        raise ValueError("Baseline version must start with '8'")
    
    # Replace first character 8 with F for experimental
    exp_version = 'F' + baseline_version[1:]
    
    # Replace positions 1-3 (000) with incremental values (121, 122, etc.)
    # This is a simplified logic - you might want to implement proper versioning
    middle_part = baseline_version[1:4]
    if middle_part == '000':
        new_middle = '121'
    elif middle_part == '300':
        new_middle = '321'
    else:
        # Increment the middle part
        try:
            middle_int = int(middle_part)
            new_middle = f"{middle_int + 121:03d}"
        except:
            new_middle = '121'
    
    exp_version = 'F' + new_middle + baseline_version[4:]
    
    return exp_version

def main():
    parser = argparse.ArgumentParser(description='Generate experimental version')
    parser.add_argument('--baseline', required=True, help='Baseline version')
    parser.add_argument('--output-version-var', required=True, help='Output variable name for version')
    parser.add_argument('--output-config-var', required=True, help='Output variable name for config file')
    
    args = parser.parse_args()
    
    try:
        exp_version = generate_experimental_version(args.baseline)
        config_file = f"config_{exp_version}.ini"
        
        # Output for GitHub Actions
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"{args.output_version_var}={exp_version}\n")
            f.write(f"{args.output_config_var}={config_file}\n")
        
        print(f"Generated experimental version: {exp_version}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
