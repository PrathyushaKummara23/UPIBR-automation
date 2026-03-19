#!/usr/bin/env python3
import argparse
import configparser
import os
import subprocess
import sys
import time

def validate_paths(config_file):
    """
    Validate all paths in the config file exist
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file)
    
    paths_to_check = []
    
    # Check SOC section paths
    if 'SOC' in config:
        for key, value in config['SOC'].items():
            if key.endswith('_file') or key in ['oobmsm', 's3m', 'icode', 'pcode-io', 'pcode-c']:
                if value and value != 'none':
                    paths_to_check.append((key, value))
    
    # Check FIT1 section paths
    if 'FIT1' in config:
        for key, value in config['FIT1'].items():
            if key in ['ucode', 'xucode', 'mcheck']:
                if value and value != 'none':
                    paths_to_check.append((key, value))
    
    missing_paths = []
    for key, path in paths_to_check:
        if not os.path.exists(path):
            missing_paths.append(f"{key}: {path}")
    
    if missing_paths:
        print("Error: The following paths do not exist:")
        for path in missing_paths:
            print(f"  - {path}")
        return False
    
    print("All paths validated successfully!")
    return True

def run_build(config_file, tools_path, exp_version):
    """
    Run the patch build process
    """
    build_script = os.path.join(tools_path, "fxtMuppt.py")
    
    if not os.path.exists(build_script):
        raise FileNotFoundError(f"Build script not found: {build_script}")
    
    cmd = ["python3", build_script, "--conf", config_file]
    
    print(f"Starting build with command: {' '.join(cmd)}")
    
    # Run the build process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Stream output in real-time
    for line in process.stdout:
        print(line.rstrip())
        
        # Check for manual signing prompts
        if "Manual SoC Patch signing" in line:
            print("🔄 SOC signing required - waiting for manual intervention...")
            # Create a marker file to indicate SOC signing is needed
            with open(f"/tmp/soc_signing_needed_{exp_version}", 'w') as f:
                f.write("SOC signing required")
            break
        elif "Press 'y' to continue" in line and "FIT1" in line:
            print("🔄 FIT1 signing required - waiting for manual intervention...")
            # Create a marker file to indicate FIT1 signing is needed
            with open(f"/tmp/fit1_signing_needed_{exp_version}", 'w') as f:
                f.write("FIT1 signing required")
            break
    
    return process

def main():
    parser = argparse.ArgumentParser(description='Build experimental patch')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--tools-path', help='Tools path')
    parser.add_argument('--exp-version', help='Experimental version')
    parser.add_argument('--validate-only', action='store_true', help='Only validate paths')
    parser.add_argument('--resume-soc', action='store_true', help='Resume after SOC signing')
    parser.add_argument('--resume-fit1', action='store_true', help='Resume after FIT1 signing')
    
    args = parser.parse_args()
    
    try:
        if args.validate_only:
            if not validate_paths(args.config):
                sys.exit(1)
            return
        
        if not args.resume_soc and not args.resume_fit1:
            # Initial build
            if not validate_paths(args.config):
                sys.exit(1)
            
            process = run_build(args.config, args.tools_path, args.exp_version)
        else:
            # Resume build
            print("Resuming build process...")
            process = run_build(args.config, args.tools_path, args.exp_version)
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code != 0:
            print(f"Build process failed with return code: {return_code}")
            sys.exit(return_code)
        
        print("Build process completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
