#!/usr/bin/env python3
import argparse
import configparser
import json
import os
import sys

def generate_config(baseline_config, exp_version, baseline_version, ocode_path, 
                   build_path, description, additional_changes, output_file):
    """
    Generate experimental debug patch configuration
    """
    
    # Read baseline config
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case
    config.read(baseline_config)
    
    # Modify DEFAULT section
    config['default']['version'] = f'0x{exp_version}'
    config['default']['build_path'] = build_path
    config['default']['patch_description'] = description
    config['default']['force'] = 'yes'
    config['default']['release'] = 'no'
    config['default']['fiv_register'] = 'no'
    config['default']['fiv_crawler'] = 'no'
    config['default']['release_notes'] = 'no'
    config['default']['prev_version'] = f'0x{baseline_version}'
    
    # Modify SOC section
    config['SOC']['soc_sign'] = 'manual'
    config['SOC']['oobmsm'] = ocode_path
    
    # Modify FIT1 section
    config['FIT1']['fit1_sign'] = 'manual'
    
    # Handle additional changes
    if additional_changes:
        try:
            changes = json.loads(additional_changes)
            for key, value in changes.items():
                if key in config['SOC']:
                    config['SOC'][key] = value
                    print(f"Updated {key} to {value}")
        except json.JSONDecodeError:
            print("Warning: Could not parse additional_changes JSON")
    
    # Write the new config file
    with open(output_file, 'w') as f:
        config.write(f)
    
    print(f"Generated config file: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate experimental patch config')
    parser.add_argument('--baseline-config', required=True, help='Baseline config file path')
    parser.add_argument('--exp-version', required=True, help='Experimental version')
    parser.add_argument('--baseline-version', required=True, help='Baseline version')
    parser.add_argument('--ocode-path', required=True, help='OCODE file path')
    parser.add_argument('--build-path', required=True, help='Build output path')
    parser.add_argument('--description', required=True, help='Patch description')
    parser.add_argument('--additional-changes', help='Additional changes JSON')
    parser.add_argument('--output', required=True, help='Output config file path')
    
    args = parser.parse_args()
    
    try:
        generate_config(
            args.baseline_config,
            args.exp_version,
            args.baseline_version,
            args.ocode_path,
            args.build_path,
            args.description,
            args.additional_changes,
            args.output
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
