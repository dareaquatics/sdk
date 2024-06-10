#!/usr/bin/env python3

import os
import subprocess
import requests
from bs4 import BeautifulSoup
import git
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, filedialog, Text
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import webbrowser

REPO_URL = 'https://github.com/dareaquatics/dare-website'
LOCAL_REPO_PATH = 'dare-website'
ASSET_DIR = 'assets/img/portfolio'

# Configure logging
logging.basicConfig(filename='editor.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def check_dependencies():
    dependencies = ['requests', 'beautifulsoup4', 'gitpython', 'pillow']
    missing_dependencies = [dep for dep in dependencies if subprocess.call(['pip', 'show', dep]) != 0]

    if missing_dependencies:
        install = messagebox.askyesno("Install Dependencies", f"Missing dependencies: {', '.join(missing_dependencies)}. Install now?")
        if install:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_dependencies])

def clone_repo(repo_url, local_path):
    if not os.path.exists(local_path):
        git.Repo.clone_from(repo_url, local_path)

def scan_html_files(repo_path):
    html_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.relpath(os.path.join(root, file), repo_path))
    return html_files

def fetch_html_content(repo_path, file_path):
    try:
        with open(os.path.join(repo_path, file_path), 'r', encoding='utf-8') as file:
            return BeautifulSoup(file, 'html.parser')
    except Exception as e:
        logging.error(f"Error fetching HTML content: {e}")
        return None

def list_editable_text(soup):
    try:
        editable_texts = {}
        unique_texts = set()
        
        for i, tag in enumerate(soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            text = tag.decode_contents().strip()
            if text and text not in unique_texts:
                editable_texts[i] = tag
                unique_texts.add(text)

        return editable_texts
    except Exception as e:
        logging.error(f"Error listing editable texts: {e}")
        return {}

def edit_text(soup, text_id, new_text, editable_texts):
    try:
        editable_texts[text_id].string = BeautifulSoup(new_text, 'html.parser')
        return soup
    except Exception as e:
        logging.error(f"Error editing text: {e}")
        return soup

def commit_changes(repo_path, commit_message, commit_description):
    try:
        repo = git.Repo(repo_path)
        repo.git.add(update=True)
        repo.index.commit(f"{commit_message}\n\n{commit_description}" if commit_description else commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except git.GitCommandError as e:
        logging.error(f"Error committing changes to git: {e}")

def upload_image(repo_path, file_path, target_dir):
    try:
        repo = git.Repo(repo_path)
        target_path = os.path.join(repo.working_tree_dir, target_dir, os.path.basename(file_path))
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        os.replace(file_path, target_path)
        repo.git.add(target_path)
        repo.index.commit(f"Add image {os.path.basename(file_path)}")
        origin = repo.remote(name='origin')
        origin.push()
    except git.GitCommandError as e:
        logging.error(f"Error uploading image to git: {e}")

def delete_image(repo_path, file_path):
    try:
        repo = git.Repo(repo_path)
        target_path = os.path.join(repo.working_tree_dir, file_path)
        os.remove(target_path)
        repo.git.add(target_path)
        repo.index.commit(f"Delete image {os.path.basename(file_path)}")
        origin = repo.remote(name='origin')
        origin.push()
    except git.GitCommandError as e:
        logging.error(f"Error deleting image from git: {e}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")

class TextEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.repo_path = LOCAL_REPO_PATH
        self.html_files = []
        self.soup = None
        self.current_file = None
        self.editable_texts = None
        self.text_changed = False

        self.title("Website Text Editor")
        self.geometry("900x700")

        self.create_widgets()
        clone_repo(REPO_URL, self.repo_path)
        self.html_files = scan_html_files(self.repo_path)
        self.populate_html_files_dropdown()

    def create_widgets(self):
        self.file_label = ttk.Label(self, text="Select the HTML file:")
        self.file_label.pack(pady=10)

        self.file_dropdown = ttk.Combobox(self, values=self.html_files, state="readonly")
        self.file_dropdown.pack(pady=5)
        self.file_dropdown.bind("<<ComboboxSelected>>", self.fetch_content)

        self.fetch_button = ttk.Button(self, text="Fetch Content", command=self.fetch_content)
        self.fetch_button.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=5)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both")

        self.text_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.text_tab, text="Edit Text")

        self.text_listbox = tk.Listbox(self.text_tab, height=15, width=80)
        self.text_listbox.pack(pady=10)

        self.edit_button = ttk.Button(self.text_tab, text="Edit Selected Text", command=self.edit_text_prompt)
        self.edit_button.pack(pady=10)

        self.commit_button = ttk.Button(self.text_tab, text="Commit Changes", command=self.commit_changes_prompt)
        self.commit_button.pack(pady=10)
        self.commit_button.config(state=tk.DISABLED)

        self.image_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.image_tab, text="Manage Images")

        self.image_note_label = ttk.Label(self.image_tab, text="Images are from assets/img/portfolio")
        self.image_note_label.pack(pady=5)

        self.upload_button = ttk.Button(self.image_tab, text="Upload Image", command=self.upload_image_prompt)
        self.upload_button.pack(pady=10)

        self.delete_button = ttk.Button(self.image_tab, text="Delete Image", command=self.delete_image_prompt)
        self.delete_button.pack(pady=10)

        self.image_listbox = tk.Listbox(self.image_tab, height=15, width=80)
        self.image_listbox.pack(pady=10)
        self.image_listbox.bind('<<ListboxSelect>>', self.preview_image)

        self.image_label = ttk.Label(self.image_tab)
        self.image_label.pack(pady=10)

        self.commit_image_button = ttk.Button(self.image_tab, text="Commit Changes", command=self.commit_changes_prompt)
        self.commit_image_button.pack(pady=10)

        self.link_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.link_tab, text="Edit Links")

        self.link_listbox = tk.Listbox(self.link_tab, height=15, width=80)
        self.link_listbox.pack(pady=10)

        self.edit_link_button = ttk.Button(self.link_tab, text="Edit Selected Link", command=self.edit_link_prompt)
        self.edit_link_button.pack(pady=10)

        self.console_log = ScrolledText(self, state='disabled', height=10)
        self.console_log.pack(fill=tk.X, padx=10, pady=10)

    def populate_html_files_dropdown(self):
        self.file_dropdown.config(values=self.html_files)

    def fetch_content(self, event=None):
        selected_file = self.file_dropdown.get()
        if selected_file:
            self.current_file = selected_file
            self.soup = fetch_html_content(self.repo_path, selected_file)
            if self.soup:
                self.editable_texts = list_editable_text(self.soup)
                self.display_texts()
                self.display_links()
                self.display_images()
                self.log("Loaded content from " + selected_file)
            else:
                messagebox.showerror("Error", "Failed to fetch HTML content.")
        else:
            messagebox.showwarning("Warning", "No HTML file selected.")

    def update_progress(self, downloaded, total_size):
        if total_size > 0:
            percentage = (downloaded / total_size) * 100
            self.progress_var.set(percentage)

    def display_texts(self):
        self.text_listbox.delete(0, tk.END)
        for i, text in self.editable_texts.items():
            self.text_listbox.insert(tk.END, f"{i}: {text.get_text()[:50]}")

    def display_links(self):
        self.link_listbox.delete(0, tk.END)
        for i, link in enumerate(self.soup.find_all('a', href=True)):
            self.link_listbox.insert(tk.END, f"{i}: {link.get_text()[:50]} ({link['href']})")

    def display_images(self):
        self.image_listbox.delete(0, tk.END)
        for root, _, files in os.walk(os.path.join(self.repo_path, ASSET_DIR)):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                    self.image_listbox.insert(tk.END, file_path)

    def edit_text_prompt(self):
        try:
            selected_index = self.text_listbox.curselection()[0]
            selected_text = self.editable_texts[selected_index].decode_contents()
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Text")

            editor = scrolledtext.ScrolledText(edit_window, wrap=tk.WORD, width=80, height=20)
            editor.pack(pady=10)
            editor.insert(tk.END, selected_text)

            save_button = ttk.Button(edit_window, text="Save", command=lambda: self.save_text(editor, selected_index, edit_window))
            save_button.pack(pady=10)
        except IndexError:
            messagebox.showwarning("Warning", "No text selected.")

    def save_text(self, editor, text_id, window):
        new_text = editor.get("1.0", tk.END).strip()
        self.soup = edit_text(self.soup, text_id, new_text, self.editable_texts)
        self.display_texts()
        window.destroy()
        self.commit_button.config(state=tk.NORMAL)
        self.text_changed = True

    def commit_changes_prompt(self):
        commit_window = tk.Toplevel(self)
        commit_window.title("Commit Changes")

        commit_message_label = ttk.Label(commit_window, text="Commit Message:")
        commit_message_label.pack(pady=5)
        commit_message_entry = ttk.Entry(commit_window, width=50)
        commit_message_entry.pack(pady=5)

        commit_description_label = ttk.Label(commit_window, text="Commit Description (optional):")
        commit_description_label.pack(pady=5)
        commit_description_text = scrolledtext.ScrolledText(commit_window, wrap=tk.WORD, width=50, height=10)
        commit_description_text.pack(pady=5)

        commit_button = ttk.Button(commit_window, text="Commit", command=lambda: self.commit_changes(commit_message_entry.get(), commit_description_text.get("1.0", tk.END).strip(), commit_window))
        commit_button.pack(pady=10)

    def commit_changes(self, message, description, window):
        if message:
            if self.text_changed:
                with open(os.path.join(self.repo_path, self.current_file), 'w', encoding='utf-8') as file:
                    file.write(str(self.soup))
            commit_changes(self.repo_path, message, description)
            window.destroy()
            messagebox.showinfo("Success", "Changes committed successfully.")
            self.commit_button.config(state=tk.DISABLED)
            self.text_changed = False
            self.log(f"Committed changes with message: {message}")
        else:
            messagebox.showerror("Error", "Commit message cannot be empty.")

    def upload_image_prompt(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            upload_image(self.repo_path, file_path, ASSET_DIR)
            self.display_images()

    def delete_image_prompt(self):
        try:
            selected_index = self.image_listbox.curselection()[0]
            file_path = self.image_listbox.get(selected_index)
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {file_path}?")
            if confirm:
                delete_image(self.repo_path, file_path)
                self.display_images()
        except IndexError:
            messagebox.showwarning("Warning", "No image selected.")

    def preview_image(self, event):
        try:
            selected_index = self.image_listbox.curselection()[0]
            file_path = os.path.join(self.repo_path, self.image_listbox.get(selected_index))
            image = Image.open(file_path)
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            logging.error(f"Error previewing image: {e}")

    def edit_link_prompt(self):
        try:
            selected_index = self.link_listbox.curselection()[0]
            link_tag = self.soup.find_all('a', href=True)[selected_index]
            current_text = link_tag.get_text()
            current_href = link_tag['href']

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Link")

            text_label = ttk.Label(edit_window, text="Link Text:")
            text_label.pack(pady=5)
            text_entry = ttk.Entry(edit_window, width=50)
            text_entry.pack(pady=5)
            text_entry.insert(tk.END, current_text)

            href_label = ttk.Label(edit_window, text="Link URL:")
            href_label.pack(pady=5)
            href_entry = ttk.Entry(edit_window, width=50)
            href_entry.pack(pady=5)
            href_entry.insert(tk.END, current_href)

            save_button = ttk.Button(edit_window, text="Save", command=lambda: self.save_link(link_tag, text_entry.get(), href_entry.get(), edit_window))
            save_button.pack(pady=10)
        except IndexError:
            messagebox.showwarning("Warning", "No link selected.")

    def save_link(self, link_tag, new_text, new_href, window):
        link_tag.string.replace_with(new_text)
        link_tag['href'] = new_href
        self.display_links()
        window.destroy()
        self.commit_button.config(state=tk.NORMAL)
        self.text_changed = True

    def log(self, message):
        self.console_log.config(state='normal')
        self.console_log.insert(tk.END, message + '\n')
        self.console_log.config(state='disabled')
        self.console_log.yview(tk.END)

if __name__ == "__main__":
    check_dependencies()
    app = TextEditorApp()
    app.mainloop()
