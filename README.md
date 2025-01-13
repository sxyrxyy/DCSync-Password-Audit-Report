# NTLM Hash Password Reuse Analyzer

## 📖 Overview
This Python script analyzes NTLM hashes from a DCSync output to detect **password reuse** across user accounts. It generates an interactive HTML report highlighting repeated hashes and associated users.

## 🚀 Features
- **Detect Password Reuse**: Identifies users sharing the same password (hash).
- **Detailed Report**: Lists masked hashes, reuse counts, and affected users.
- **Summary Table**: Quick view of hashes and their reuse frequency.
- **Dark Mode**: Toggle for better readability.
- **Interactive Hash Reveal**: Click to reveal full hashes.

## 📂 Usage
1. **Run the Script:**
   ```bash
   python script.py <dc-sync-output-file>
   ```
   Replace `<dc-sync-output-file>` with your NTLM hash file.

**Quickly detect password reuse in NTLM hashes! 🔍**

