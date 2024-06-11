# DARE Aquatics Manual News Entry Script Documentation

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

This script allows users to manually input, edit, and add news entries to the DARE Aquatics website. It collects news items from the user, generates HTML content, updates the local HTML file, and pushes the changes to GitHub.

---

## Prerequisites

Before running the script, ensure you have the following:
- Python 3.6 or later installed.
- Git installed.
- Internet connection for pushing changes to GitHub.

---

## Download and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dareaquatics/sdk
cd sdk/manualsync
```

### 2. Install Dependencies
Run the following command to install required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set File Path and Repository Path
Ensure the `FILE_PATH` and `LOCAL_REPO_PATH` constants in the script point to the correct locations of your local HTML file and repository.

### 4. Run the Script
Execute the script using Python:
```bash
python3 manual_news_entry.py
```

---

## Script Overview

The script performs several tasks to update the DARE Aquatics website manually:
1. Collects news items from the user.
2. Generates HTML content from the collected news items.
3. Updates the local HTML file with the new content.
4. Commits the changes to the local Git repository and pushes them to GitHub.

### Key Components
- **Input Handling**: For collecting news items from the user.
- **HTML Generation**: For creating HTML content from news items.
- **File Operations**: For updating the HTML file.
- **GitPython**: For interacting with the Git repository.

---

## Functions and Classes

### 1. input_news_items()
Collects news items from the user through the console input.

#### Parameters:
- None

#### Returns:
- `news_items` (list): A list of dictionaries, each containing the title, date, and content of a news item.

#### Example:
```python
news_items = input_news_items()
```

### 2. generate_html(news_items)
Generates HTML content for the collected news items.

#### Parameters:
- `news_items` (list): A list of dictionaries containing news item data.

#### Returns:
- `news_html` (str): A string of HTML content.

#### Example:
```python
news_html = generate_html(news_items)
```

### 3. update_html_file(news_html)
Updates the local HTML file with the generated news HTML content.

#### Parameters:
- `news_html` (str): The HTML content to insert into the file.

#### Example:
```python
update_html_file(news_html)
```

### 4. push_to_github()
Commits the changes to the local Git repository and pushes them to GitHub.

#### Parameters:
- None

#### Example:
```python
push_to_github()
```

### 5. main()
Main function that orchestrates the manual update process. It collects news items, generates HTML, updates the HTML file, and pushes the changes to GitHub.

#### Parameters:
- None

#### Example:
```python
if __name__ == "__main__":
    main()
```

---

## Usage Instructions

### Manually Adding News Entries
1. Ensure you have cloned the repository and installed the dependencies.
2. Set the `FILE_PATH` and `LOCAL_REPO_PATH` constants in the script to the correct locations.
3. Run the script using `python3 manual_news_entry.py`.
4. Follow the prompts to input news items:
    - Enter the title of the news item.
    - Enter the date in MM-DD-YYYY format.
    - Enter the content of the news item.
5. The script will generate the HTML, update the HTML file, and push the changes to GitHub.

### Logs and Progress
- The script prints progress messages to the console to inform the user of each step being performed.

---

## Troubleshooting

### Common Issues

#### Invalid Date Format
Ensure the date is entered in MM-DD-YYYY format.

#### File Not Found
Ensure the `FILE_PATH` points to the correct location of the local HTML file.

#### Git Command Errors
Ensure you have Git installed and the repository URL is correct.

### Logs
Check the console output for detailed error messages and logs.

---

## Appendix

### Dependencies
- `gitpython`

### Commands
- **Clone Repository**: `git clone https://github.com/dareaquatics/sdk`
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Script**: `python3 manualsync.py`

---
