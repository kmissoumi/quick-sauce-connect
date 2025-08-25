#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple Flask web application that works with the 'flask run' command.
- Displays a mobile-friendly demo page with client info.
- Optionally shares a directory with full subfolder navigation, specified by the
  DEMO_SHARE environment variable.
"""

import os
from html import escape
from urllib.parse import quote
from flask import Flask, request, send_from_directory, abort, url_for

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Configure the shared path from an Environment Variable ---
shared_path_from_env = os.environ.get('DEMO_SHARE')
if shared_path_from_env:
    abs_path = os.path.abspath(shared_path_from_env)
    if not os.path.isdir(abs_path):
        # For subfolder browsing, the path MUST be a directory.
        raise NotADirectoryError(f"The path specified in DEMO_SHARE is not a directory: {abs_path}")
    
    app.config['SHARED_PATH'] = abs_path
    print(f"✅ File sharing enabled. Path: {app.config['SHARED_PATH']}")
else:
    app.config['SHARED_PATH'] = None
    print("ℹ️ File sharing is disabled. To enable, set the DEMO_SHARE environment variable.")


# --- Style and HTML Templates ---
CSS_STYLE = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    margin: 0;
    background-color: #f4f4f9;
    color: #333;
}
.container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 1rem 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
h1, h2 {
    color: #0056b3;
    border-bottom: 2px solid #eee;
    padding-bottom: 0.5rem;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
}
th, td {
    text-align: left;
    padding: 12px 15px;
    border-bottom: 1px solid #ddd;
}
th {
    background-color: #007bff;
    color: white;
}
a {
    color: #0066cc;
    text-decoration: none;
    font-weight: 500;
}
a:hover {
    text-decoration: underline;
}
.dir::before { content: "📁 "; }
.file::before { content: "📄 "; }
.parent::before { content: "⬆️ "; }
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {style_block}
    </style>
</head>
<body>
    <div class="container">
        {content_block}
    </div>
</body>
</html>
"""

def get_secure_path(subpath):
    """
    Validates that the requested subpath is within the shared directory.
    Prevents directory traversal attacks.
    """
    base_dir = app.config.get('SHARED_PATH')
    if not base_dir:
        abort(404, "File sharing is not enabled.")

    # Securely join the paths and resolve any '..' components
    requested_path = os.path.realpath(os.path.join(base_dir, subpath))

    # Check if the resolved path is still within the base directory
    if os.path.commonprefix([requested_path, base_dir]) != base_dir:
        abort(403) # Forbidden

    return requested_path


@app.route("/")
def main_page():
    ua = request.user_agent
    client_info_html = "<h1>Welcome!</h1><table>"
    client_info_html += f"<tr><th>Attribute</th><th>Value</th></tr>"
    client_info_html += f"<tr><td>IP Address</td><td>{escape(request.remote_addr)}</td></tr>"
    client_info_html += f"<tr><td>Browser</td><td>{escape(ua.browser or 'N/A')} {escape(ua.version or '')}</td></tr>"
    client_info_html += f"<tr><td>Platform (OS)</td><td>{escape(ua.platform or 'N/A')}</td></tr>"
    client_info_html += f"<tr><td>User Agent String</td><td>{escape(ua.string)}</td></tr>"
    client_info_html += "</table>"
    
    share_html = ""
    if app.config.get('SHARED_PATH'):
        share_html = f'<h2>Shared Files</h2><p><a href="{url_for("browse_path")}">Browse shared files</a></p>'

    full_content = client_info_html + share_html
    return HTML_TEMPLATE.format(
        title="Flask Demo",
        style_block=CSS_STYLE, 
        content_block=full_content
    )


@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse_path(subpath=""):
    secure_dir_path = get_secure_path(subpath)

    if not os.path.isdir(secure_dir_path):
        # If the path is a file, redirect to download it
        return url_for('download_file', subpath=subpath)

    dir_listing_html = f"<h2>Browsing: /{escape(subpath)}</h2><table><tr><th>Name</th></tr>"

    # Add a link to the parent directory
    if subpath:
        parent_path = os.path.dirname(subpath.strip('/'))
        dir_listing_html += f'<tr><td><a href="{url_for("browse_path", subpath=parent_path)}" class="parent">Parent Directory</a></td></tr>'

    # Separate and sort directories and files
    dirs, files = [], []
    with os.scandir(secure_dir_path) as it:
        for entry in it:
            if entry.is_dir():
                dirs.append(entry.name)
            else:
                files.append(entry.name)
    
    # List directories first, then files
    for name in sorted(dirs, key=str.lower):
        item_subpath = os.path.join(subpath, name)
        dir_listing_html += f'<tr><td><a href="{url_for("browse_path", subpath=item_subpath)}" class="dir">{escape(name)}/</a></td></tr>'
    
    for name in sorted(files, key=str.lower):
        item_subpath = os.path.join(subpath, name)
        dir_listing_html += f'<tr><td><a href="{url_for("download_file", subpath=item_subpath)}" class="file">{escape(name)}</a></td></tr>'

    dir_listing_html += "</table>"
    
    return HTML_TEMPLATE.format(
        title=f"Browsing /{escape(subpath)}",
        style_block=CSS_STYLE,
        content_block=dir_listing_html
    )


@app.route('/download/<path:subpath>')
def download_file(subpath):
    secure_file_path = get_secure_path(subpath)

    if not os.path.isfile(secure_file_path):
        abort(404, "File not found.")

    directory = os.path.dirname(secure_file_path)
    filename = os.path.basename(secure_file_path)

    return send_from_directory(directory, filename, as_attachment=True)