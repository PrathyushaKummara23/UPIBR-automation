"""
OSPL - On-the-Spot Patch Loading
Loads Intel microcode (.inc file) onto a running SRF Linux system via SSH.

Usage:
    python ospl.py <ip_address> <username> <password> <patch_file_path>

Example:
    python ospl.py 10.138.186.199 root intel@123 "/root/m_01_a06f3_830003b6.inc"
"""

import sys
import os
import paramiko
from scp import SCPClient


def remote_deploy_and_update(pc2_ip, username, password, patch_path):

    patch_filename = os.path.basename(patch_path)   # e.g. m_01_a06f3_830003b6.inc
    remote_staging = "/root"
    remote_patch   = f"{remote_staging}/{patch_filename}"
    ospl_dir       = "/root/OSPL"
    ucode_dir      = "/lib/firmware/intel-ucode"

    print(f"\n{'='*55}")
    print(f"  OSPL - On-the-Spot Patch Loading")
    print(f"{'='*55}")
    print(f"  Target System : {pc2_ip}")
    print(f"  Username      : {username}")
    print(f"  Patch File    : {patch_filename}")
    print(f"{'='*55}\n")

    # ── Connect via SSH ───────────────────────────────────────────
    # NOTE: AutoAddPolicy is used here for internal SRF lab systems where
    # host keys are not pre-registered. This is an accepted security
    # trade-off in a controlled lab network environment.
    print("🔌 Connecting to SRF system via SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(pc2_ip, username=username, password=password, timeout=30)
    print("✅ SSH connection established\n")

    # ── SCP: Copy .inc file to SRF /root/ ────────────────────────
    print(f"📤 Copying {patch_filename} → {pc2_ip}:{remote_patch}")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(patch_path, remote_patch)
    print("✅ File transferred successfully\n")

    # ── OSPL Command Sequence ─────────────────────────────────────
    commands = [
        ("1. Check microcode BEFORE",
         "dmesg | grep -i microcode | tail -5 || true"),

        ("2. Enable downgrade mode",
         "echo 1 > /sys/kernel/debug/microcode/downgrade"),

        ("3. Stage patch file",
         f"mkdir -p {ospl_dir} && cp {remote_patch} {ospl_dir}/ && rm -f {remote_patch}"),

        ("4. Clear old microcode",
         f"rm -f {ucode_dir}/*"),

        ("5. Deploy new microcode",
         f"cp {ospl_dir}/{patch_filename} {ucode_dir}/"),

        ("6. Verify firmware directory",
         f"ls -lh {ucode_dir}/"),

        ("7. Load via iucode_tool",
         f"iucode_tool -K {ucode_dir}"),

        ("8. Trigger CPU reload",
         "echo 1 > /sys/devices/system/cpu/microcode/reload"),

        ("9. Disable downgrade mode",
         "echo 0 > /sys/kernel/debug/microcode/downgrade"),

        ("10. Verify microcode AFTER",
         "dmesg | grep -i microcode | tail -10"),
    ]

    print("🚀 Starting OSPL sequence...\n")
    for step_name, cmd in commands:
        print(f"▶  {step_name}")
        print(f"   $ {cmd}")

        stdin, stdout, stderr = ssh.exec_command(cmd)
        out  = stdout.read().decode().strip()
        err  = stderr.read().decode().strip()
        code = stdout.channel.recv_exit_status()

        if out:
            for line in out.splitlines():
                print(f"   {line}")
        if err:
            for line in err.splitlines():
                print(f"   [stderr] {line}")

        if code != 0:
            print(f"\n❌ Step failed: '{step_name}' (exit code {code})")
            ssh.close()
            sys.exit(code)

        print(f"   ✅ Done\n")

    ssh.close()
    print("=" * 55)
    print("✅  OSPL completed successfully!")
    print(f"    Patch '{patch_filename}' is now live on {pc2_ip}")
    print("=" * 55)


# ── Entry Point ───────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("\nUsage:")
        print("  python ospl.py <ip> <username> <password> <patch_file_path>")
        print("\nExample:")
        print('  python ospl.py 10.138.186.199 root intel@123 "/root/m_01_a06f3_830003b6.inc"')
        sys.exit(1)

    pc2_ip     = sys.argv[1]
    username   = sys.argv[2]
    password   = sys.argv[3]
    patch_path = sys.argv[4]

    if not os.path.isfile(patch_path):
        print(f"\n❌ Error: Patch file not found: {patch_path}")
        sys.exit(1)

    if not patch_path.lower().endswith(".inc"):
        print(f"\n❌ Error: Expected a .inc microcode patch file, got: {patch_path}")
        sys.exit(1)

    remote_deploy_and_update(pc2_ip, username, password, patch_path)
