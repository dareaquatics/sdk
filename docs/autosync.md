# DARE Aquatics Website Local Update Script Documentation

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

This script is designed to run locally and is intended to sync news updates from the DARE Aquatics website with the associated GitHub repository. It fetches news articles from the website, generates HTML content, updates the local HTML file, and pushes the changes to GitHub.

---

## Prerequisites

Before running the script, ensure you have the following:
- Python 3 or later installed.
- Git installed (or the script will attempt to download a portable version).
- Internet connection for downloading Git, fetching news, and pushing changes to GitHub.

---

## Download and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dareaquatics/sdk
cd sdk/autosync
```

### 2. Install Dependencies
Run the following command to install required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set GitHub Token
Ensure you have a valid GitHub token set in the script (`GITHUB_TOKEN` variable). It should be a Classic GitHub Personal Access token with `repo` perms.

### 4. Run the Script
Execute the script using Python:
```bash
python3 autosync.py
```

---

## Script Overview

The script performs several tasks to update the DARE Aquatics website:
1. Validates the GitHub token.
2. Checks if Git is installed; if not, downloads a portable version.
3. Clones the repository if it doesn't exist locally.
4. Fetches news articles from the DARE Aquatics website.
5. Generates HTML content from the news articles.
6. Updates the local HTML file with the new content.
7. Pushes the changes to GitHub.

### Key Components
- **Requests**: For making HTTP requests.
- **BeautifulSoup**: For parsing and manipulating HTML content.
- **GitPython**: For interacting with the Git repository.
- **Cloudscraper**: To bypass web scraping protections.
- **TQDM**: For displaying progress bars.
- **Logging**: For capturing and displaying logs.

---

## Functions and Classes

### 1. check_git_installed()
Checks if Git is installed on the system. If not found, it logs a warning and attempts to download a portable version.

### 2. download_portable_git()
Downloads a portable version of Git based on the operating system. Supports Windows, Linux, and macOS.

### 3. is_repo_up_to_date(repo_path)
Checks if the local Git repository is up-to-date with the remote repository.

### 4. delete_and_reclone_repo(repo_path)
Deletes the local repository and reclones it from the remote repository.

### 5. clone_repository()
Clones the GitHub repository to the local machine. If the repository already exists, it checks if it's up-to-date and reclones if necessary.

### 6. check_github_token_validity()
Validates the GitHub token by making a request to the GitHub API.

### 7. fetch_news()
Fetches news articles from the DARE Aquatics website using a scraper. Parses the HTML content and extracts relevant information.

### 8. convert_links_to_clickable(text)
Converts plain text URLs into clickable HTML links.

### 9. generate_html(news_items)
Generates HTML content for the news articles.

### 10. update_html_file(news_html)
Updates the local HTML file with the generated news HTML content.

### 11. push_to_github()
Pushes the changes to the GitHub repository.

### 12. main()
Main function that orchestrates the update process. It performs all the necessary steps in sequence.

---

## Usage Instructions

### Fetching News and Updating the Website
1. Ensure you have cloned the repository and installed the dependencies.
2. Run the script using `python3 update_script.py`.
3. The script will perform all necessary actions to update the news section of the website and push the changes to GitHub.

### Logs and Progress
- The script uses colored logging to display information, warnings, and errors.
- Progress bars are displayed for downloading Git, cloning the repository, committing changes, and pushing changes to GitHub.

---

## Troubleshooting

### Common Issues

#### Missing Dependencies
If dependencies are missing, install them using the provided `requirements.txt` file.

#### Git Not Installed
If Git is not installed, the script will attempt to download a portable version. Ensure you have an internet connection.

#### Invalid GitHub Token
Ensure the `GITHUB_TOKEN` variable is set to a valid GitHub token.

#### Repository Cloning Errors
Ensure the repository URL is correct and you have necessary permissions.

### Logs
Check the log output for detailed error messages and logs.

---

## Appendix

### Dependencies
- `requests`
- `beautifulsoup4`
- `gitpython`
- `cloudscraper`
- `colorlog`
- `tqdm`

### Commands
- **Clone Repository**: `git clone <https://github.com/dareaquatics/sdk>`
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Script**: `python3 autosync.py`

