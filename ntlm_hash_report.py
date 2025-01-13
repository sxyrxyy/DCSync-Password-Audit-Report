import collections
import os
import sys
from datetime import datetime


def generate_html_report(hash_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sorted_hash_data = dict(sorted(hash_data.items(), key=lambda item: len(item[1]), reverse=True))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NTLM Hash Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; transition: background-color 0.3s, color 0.3s; }}
            .container {{ max-width: 1400px; margin: auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); transition: background-color 0.3s; }}
            h1, h2 {{ text-align: center; color: #333; transition: color 0.3s; }}
            table {{ border-collapse: collapse; margin-top: 20px; width: 100%; }}
            th, td {{ padding: 12px 24px; border-bottom: 1px solid #ddd; text-align: center; vertical-align: top; word-break: break-word; }}
            th {{ background-color: #5D3FD3; color: white; font-size: 16px; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .user-list {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }}
            .user-badge {{ background-color: #D6C8FF; color: #333; border-radius: 12px; padding: 6px 14px; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .toggle-btn, .dark-mode-btn {{ background-color: #5D3FD3; color: white; border: none; padding: 6px 14px; cursor: pointer; border-radius: 5px; font-size: 14px; width: auto; text-align: center; font-family: monospace; }}
            .dark-mode-btn {{ position: fixed; top: 20px; right: 20px; }}

            /* Dark Mode Styles */
            body.dark-mode {{ background-color: #1e1e1e; color: #f1f1f1; }}
            .container.dark-mode {{ background-color: #2e2e2e; }}
            h1.dark-mode, h2.dark-mode {{ color: #D6C8FF; }}
            table.dark-mode th {{ background-color: #5D3FD3; color: white; }}
            table.dark-mode tr:hover {{ background-color: #555; }}
            .user-badge.dark-mode {{ background-color: #5D3FD3; color: #f1f1f1; }}
            .toggle-btn.dark-mode {{ background-color: #5D3FD3; color: #f1f1f1; }}
        </style>
        <script>
            function toggleHash(button) {{
                var maskedHash = button.getAttribute('data-masked');
                var fullHash = button.getAttribute('data-full');
                button.innerText = (button.innerText === maskedHash) ? fullHash : maskedHash;
            }}

            function toggleDarkMode() {{
                document.body.classList.toggle('dark-mode');
                document.querySelector('.container').classList.toggle('dark-mode');
                document.querySelectorAll('h1, h2').forEach(header => header.classList.toggle('dark-mode'));
                document.querySelectorAll('table').forEach(table => table.classList.toggle('dark-mode'));
                document.querySelectorAll('.user-badge').forEach(badge => badge.classList.toggle('dark-mode'));
                document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.toggle('dark-mode'));
            }}
        </script>
    </head>
    <body>
        <button class="dark-mode-btn" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        <div class="container">
            <h1>NTLM Hash Analysis Report</h1>
            <p>Generated on: {timestamp}</p>

            <table>
                <tr>
                    <th style="width: 40ch;">NTLM Hash</th>
                    <th style="width: 8ch;">Count</th>
                    <th>Users</th>
                </tr>
    """

    for ntlm_hash, users in sorted_hash_data.items():
        masked_hash = ntlm_hash[:4] + '*' * (len(ntlm_hash) - 8) + ntlm_hash[-4:]
        user_badges = ''.join([f'<span class="user-badge">{user}</span>' for user in users])
        html_content += f"""
                <tr>
                    <td>
                        <button class="toggle-btn" data-masked="{masked_hash}" data-full="{ntlm_hash}" onclick="toggleHash(this)">{masked_hash}</button>
                    </td>
                    <td><strong>{len(users)}</strong></td>
                    <td><div class="user-list">{user_badges}</div></td>
                </tr>
        """

    html_content += """
            </table>
            <h2>Summary of Hash Counts</h2>
            <table>
                <tr>
                    <th style="width: 40ch;">NTLM Hash</th>
                    <th style="width: 8ch;">Count</th>
                </tr>
    """

    for ntlm_hash, users in sorted_hash_data.items():
        masked_hash = ntlm_hash[:4] + '*' * (len(ntlm_hash) - 8) + ntlm_hash[-4:]
        html_content += f"""
                <tr>
                    <td>
                        <button class="toggle-btn" data-masked="{masked_hash}" data-full="{ntlm_hash}" onclick="toggleHash(this)">{masked_hash}</button>
                    </td>
                    <td><strong>{len(users)}</strong></td>
                </tr>
        """

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """
    return html_content


def analyze_ntlm_hashes(file_path):
    hash_users = collections.defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 4:
                username = parts[0]
                ntlm_hash = parts[3]
                hash_users[ntlm_hash].append(username)
    return {k: v for k, v in hash_users.items() if len(v) > 1}


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <dc-sync-filename>")
        return

    input_file = sys.argv[1]
    output_file = 'ntlm_hash_report.html'

    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    reused_hashes = analyze_ntlm_hashes(input_file)
    html_report = generate_html_report(reused_hashes)

    with open(output_file, 'w') as file:
        file.write(html_report)

    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    main()
