#!/usr/bin/env python3
"""
Helper script to guide users through setting up email notifications
"""

def main():
    print("📧 Email Notifications Setup Guide")
    print("=" * 50)
    print()
    
    print("Step 1: Determine Your Email Settings")
    print("For Intel employees, you can typically use:")
    print("- SMTP Server: smtp.intel.com")
    print("- SMTP Port: 587")
    print("- From Email: your.email@intel.com")
    print("- To Email: your.email@intel.com (or team email)")
    print()
    
    print("Step 2: Add Email Secrets to GitHub")
    print("1. Go to your GitHub repository")
    print("2. Click Settings → Secrets and variables → Actions")
    print("3. Add these secrets:")
    print("   - FROM_EMAIL: your.email@intel.com")
    print("   - NOTIFICATION_EMAIL: recipient@intel.com")
    print("   - SMTP_USERNAME: your.username (optional)")
    print("   - SMTP_PASSWORD: your.password (optional)")
    print()
    
    print("Step 3: Test Email Setup")
    print("You can test email sending with:")
    print("echo 'Test message' | mail -s 'Test Subject' your.email@intel.com")
    print()
    
    print("Step 4: Enable Notifications in Workflow")
    print("When running the workflow:")
    print("- Check 'Enable notifications' box")
    print("- Or set enable_notifications to 'true'")
    print()
    
    print("✅ Setup complete! Your workflow will now send email notifications.")
    print()
    
    print("Email Notification Types:")
    print("- 🚀 Build start notification")
    print("- 🔐 Manual signing required (SOC and FIT1)")
    print("- ✅ Build completion (success)")
    print("- ❌ Build failure notification")

if __name__ == "__main__":
    main()
