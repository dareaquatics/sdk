# DARE Aquatics Website Editor Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Download and Setup](#download-and-setup)
4. [Script Overview](#script-overview)
5. [Functions and Classes](#functions-and-classes)
6. [Usage Instructions](#usage-instructions)
7. [Troubleshooting](#troubleshooting)
8. [Appendix](#appendix)

---

## Introduction

The DARE Aquatics Website Editor is a comprehensive GUI tool designed to streamline the process of editing HTML content, managing images, and committing changes to the DARE Aquatics website repository. It leverages several Python libraries to facilitate these tasks, making it easier for non-developers to update and maintain the website.

---

## Prerequisites

Before using the DARE Aquatics Website Editor, ensure you have the following:
- Python 3 or later installed.
- Git installed.
- Internet connection for cloning the repository and installing dependencies.

---

## Download and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dareaquatics/sdk
cd sdk/editor
```

### 2. Install Dependencies
Run the following command to install required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Execute the script using Python:
```bash
python3 editor.py
```

---

## Script Overview

The DARE Aquatics Website Editor is built using Tkinter for the GUI, BeautifulSoup for HTML parsing, and GitPython for repository management. It provides a user-friendly interface for editing text, managing images, and committing changes to the Git repository.

### Key Components
- **Tkinter**: For the graphical user interface.
- **BeautifulSoup**: For parsing and manipulating HTML content.
- **GitPython**: For interacting with the Git repository.
- **Logging**: For capturing and displaying logs within the GUI.

---

## Functions and Classes

### TextEditorApp Class

This is the main class that initializes the application and handles user interactions.

#### Methods:

1. **__init__()**: Initializes the application, sets up the GUI, and initializes the repository.
2. **create_widgets()**: Creates and arranges the widgets in the GUI.
3. **set_log_level(event)**: Sets the log level based on user selection.
4. **log_message(message, level)**: Logs messages to the console.
5. **update_directory_overview()**: Updates the directory overview panel.
6. **generate_tree_view(startpath)**: Generates a tree view of the directory.
7. **init_repo()**: Clones the repository and initializes the application state.
8. **populate_html_files_dropdown()**: Populates the dropdown with HTML files.
9. **fetch_content(event)**: Fetches the content of the selected HTML file.
10. **display_texts()**: Displays editable texts in the listbox.
11. **display_links()**: Displays links in the listbox.
12. **display_images()**: Displays images in the listbox.
13. **edit_text_prompt()**: Opens a prompt to edit selected text.
14. **save_text(editor, text_id, window)**: Saves the edited text.
15. **add_text_prompt()**: Opens a prompt to add new text.
16. **add_text(tag, text, window)**: Adds new text to the HTML.
17. **commit_changes_prompt()**: Opens a prompt to commit changes.
18. **commit_changes(message, description, window)**: Commits changes to the repository.
19. **upload_image_prompt()**: Opens a file dialog to upload an image.
20. **delete_image_prompt()**: Deletes the selected image.
21. **preview_image(event)**: Previews the selected image.
22. **edit_link_prompt()**: Opens a prompt to edit a selected link.
23. **save_link(link_tag, new_text, new_href, window)**: Saves the edited link.
24. **populate_styling_help()**: Populates the styling help tab with HTML tags.
25. **populate_commit_history()**: Populates the commit history listbox.
26. **show_commit_details(event)**: Shows details of the selected commit.

### Helper Functions

1. **log_message(console, message, level)**: Logs messages to the console.
2. **check_and_install_dependencies(console)**: Checks for and installs missing dependencies.
3. **clone_repo(repo_url, local_path, console)**: Clones the repository from the given URL.
4. **fetch_html_files(repo_path)**: Fetches HTML files from the repository.
5. **fetch_html_content(repo_path, file_path)**: Fetches and parses HTML content from a file.
6. **list_editable_text(soup)**: Lists editable texts from the HTML content.
7. **edit_text(soup, text_id, new_text, editable_texts)**: Edits text in the HTML content.
8. **add_text(soup, tag_name, new_text)**: Adds new text to the HTML content.
9. **save_html_content(file_path, soup, original_content)**: Saves HTML content to a file.
10. **pull_latest_changes(repo_path, console)**: Pulls the latest changes from the repository.
11. **commit_changes(repo_path, commit_message, commit_description, console)**: Commits changes to the repository.
12. **upload_image(repo_path, file_path, target_dir, console)**: Uploads an image to the repository.
13. **delete_image(repo_path, file_path, console)**: Deletes an image from the repository.

---

## Usage Instructions

### Editing Text
1. Select an HTML file from the dropdown.
2. Click "Edit Selected Text" to modify the text.
3. Click "Commit Changes" to save and commit your changes.

### Managing Images
1. Click "Upload Image" to add a new image.
2. Select an image and click "Delete Image" to remove it.
3. Click "Commit Changes" to save and commit your changes.

### Editing Links
1. Select an HTML file from the dropdown.
2. Click "Edit Selected Link" to modify a link.
3. Click "Commit Changes" to save and commit your changes.

### Viewing Commit History
1. Navigate to the "Commit History" tab.
2. Select a commit to view its details.

### Updating Directory Overview
1. Navigate to the "Directory Overview" tab.
2. Click "Update" to refresh the view.

---

## Troubleshooting

### Common Issues

#### Missing Dependencies
If dependencies are missing, the application will prompt to install them. Ensure you have an active internet connection.

#### Repository Cloning Errors
Ensure you have the correct repository URL and necessary permissions to clone the repository.

#### Commit Errors
Ensure you have the correct permissions to commit to the repository and that your local repository is up-to-date.

### Logs
Check the log panel at the bottom of the application for detailed error messages and logs.

---

## Appendix

### Dependencies
- `requests`
- `beautifulsoup4`
- `gitpython`
- `pillow`

### Commands
- **Clone Repository**: `git clone <https://github.com/dareaquatics/sdk>`
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Application**: `python3 editor.py`

---

