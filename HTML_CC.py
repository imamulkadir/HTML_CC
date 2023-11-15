import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import filedialog
from bs4 import BeautifulSoup
import re
import difflib
import os
from tkinter import messagebox

def extract_visible_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all script and style tags
    for script in soup(['script', 'style']):
        script.extract()

    # Get the text content
    text_content = soup.get_text()

    # Normalize the text by removing extra spaces and newlines
    text_content = re.sub(r'\s+', ' ', text_content).strip()

    return text_content

def compare_text():
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()

    with open(file1_path, 'r', encoding='utf-8') as file1:
        text1 = extract_visible_text(file1.read())

    with open(file2_path, 'r', encoding='utf-8') as file2:
        text2 = extract_visible_text(file2.read())

    if text1 == text2:
        # No mismatch found
        messagebox.showinfo("No Mismatch", "No mismatch found")
    else:
        # Mismatch found
        differ = difflib.Differ()
        diff = list(differ.compare(text1.split(), text2.split()))

        file1_mismatches = []
        file2_mismatches = []

        for line in diff:
            if line.startswith('- '):
                file1_mismatches.append(line[2:])
            elif line.startswith('+ '):
                file2_mismatches.append(line[2:])

        # Get the file names without path
        file1_name = os.path.basename(file1_path)
        file2_name = os.path.basename(file2_path)

        # Create a popup window for displaying mismatched text in a table
        popup_window = tk.Toplevel()
        popup_window.title("Mismatched Text")

        # Get the screen width and height
        screen_width = popup_window.winfo_screenwidth()
        screen_height = popup_window.winfo_screenheight()

        # Calculate the x and y coordinates for the center of the screen
        x = (screen_width - 513) // 2
        y = (screen_height - 513) // 2

        # Set the window size and position
        popup_window.geometry(f"513x513+{x}+{y}")

        # Create a table using ttk.Treeview
        table = ttk.Treeview(popup_window, columns=(file1_name, file2_name), show="headings")
        table.heading(file1_name, text=file1_name)
        table.heading(file2_name, text=file2_name)

        # Set the cell content to be centered
        table.column(file1_name, anchor='center')
        table.column(file2_name, anchor='center')
        table.pack()

        # Populate the table with mismatched words
        max_len = max(len(file1_mismatches), len(file2_mismatches))

        for i in range(max_len):
            file1_word = file1_mismatches[i] if i < len(file1_mismatches) else ""
            file2_word = file2_mismatches[i] if i < len(file2_mismatches) else ""
            table.insert("", "end", values=(file1_word, file2_word))

def browse_file1():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.htm *.html")])
    file1_entry.delete(0, tk.END)
    file1_entry.insert(0, file_path)

def browse_file2():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.htm *.html")])
    file2_entry.delete(0, tk.END)
    file2_entry.insert(0, file_path)

# Function to extract words from HTML content
def extract_words(file_path, listbox, label, word_count_label):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    words = soup.get_text().split()
    
    listbox.delete(0, tk.END)
    for word in words:
        listbox.insert(tk.END, word)

    # Display the total word count along with the label
    label.config(text=f"{label['text']} {len(words)}")

#Function to open fb profile
def open_facebook_profile():
    webbrowser.open("https://www.facebook.com/imamulkadir")

# Create the main window
root = tk.Tk()
root.title("HTML Content Comparison")

# Create two buttons to open HTML files
def open_and_display_file(button_num, listbox, label, word_count_label):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    if button_num == 1:
        label.config(text="File 1:")
        extract_words(file_path, listbox, label, word_count_label)
    elif button_num == 2:
        label.config(text="File 2:")
        extract_words(file_path, listbox, label, word_count_label)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the center of the screen
x = (screen_width - 650) // 2
y = (screen_height - 500) // 2

# Set the window size and position
root.geometry(f"650x500+{x}+{y}")

# Create a notebook (tabs) for the two functionalities
notebook = ttk.Notebook(root)

# Create the first tab for text comparison
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="HTML File Comparison")

file1_label = tk.Label(tab1, text="Select File 1")
file1_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
file1_entry = tk.Entry(tab1, width=50)
file1_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button1 = ttk.Button(tab1, text="Browse", command=browse_file1, style='Rounded.TButton', cursor="hand2")
browse_button1.grid(row=0, column=2, padx=10, pady=5)

file2_label = tk.Label(tab1, text="Select File 2")
file2_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
file2_entry = tk.Entry(tab1, width=50)
file2_entry.grid(row=1, column=1, padx=10, pady=5)
browse_button2 = ttk.Button(tab1, text="Browse", command=browse_file2, style='Rounded.TButton', cursor="hand2")
browse_button2.grid(row=1, column=2, padx=10, pady=5)

compare_button = ttk.Button(tab1, text="Compare Files", command=compare_text, style='Rounded.TButton', cursor="hand2")
compare_button.grid(row=2, column=0, columnspan=3, pady=10)

# Create the second tab for HTML word extraction
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="HTML Word Extraction")

frame1 = tk.Frame(tab2)
frame1.pack()

# Create two buttons to open HTML files with the rounded style
button1 = ttk.Button(frame1, text="Browse File 1", command=lambda: open_and_display_file(1, listbox1, label1, word_count_label1), style='Rounded.TButton', cursor="hand2")
button2 = ttk.Button(frame1, text="Browse File 2", command=lambda: open_and_display_file(2, listbox2, label2, word_count_label2), style='Rounded.TButton', cursor="hand2")
button1.grid(row=0, column=0, padx=5)
button2.grid(row=0, column=1, padx=5)

listbox1 = tk.Listbox(tab2, width=40)
listbox2 = tk.Listbox(tab2, width=40)
listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

label1 = tk.Label(tab2, text="File 1:", anchor="w")
label2 = tk.Label(tab2, text="File 2:", anchor="w")
label1.pack(fill="x")
label2.pack(fill="x")

word_count_label1 = tk.Label(tab2, text="", anchor="w")
word_count_label2 = tk.Label(tab2, text="", anchor="w")
word_count_label1.pack(fill="x")
word_count_label2.pack(fill="x")

notebook.pack()

# Style for rounded buttons
style = ttk.Style()
style.configure('Rounded.TButton', cornerradius=10)

# Add the footer label with a link to your Facebook profile
footer_label = tk.Label(root, text="©2023 - Imamul Kadir", cursor="hand2", fg="#427D9D", font=("Poppins semiBold", 10))
footer_label.pack(side=tk.BOTTOM, padx=10, pady=5)

# Bind the label to the function that opens the link
footer_label.bind("<Button-1>", lambda event: open_facebook_profile())

root.mainloop()