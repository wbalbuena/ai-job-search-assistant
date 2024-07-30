import os
from datetime import datetime
import PyPDF2
import google.generativeai as genai

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# --- API KEY ---
# SET ENVIRONMENTAL VARIABLE "GOOGLE_API_KEY" TO YOUR GOOGLE API KEY BEFORE RUNNING
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
print("GOOGLE_API_KEY="+GOOGLE_API_KEY)
# ----------------

# --- GOOGLE GEMINI MODEL ---
# Swap models when rate limited - 1.0 has no output token limit, unlikely to hit the high RPD
#chosen_model='gemini-1.0-pro'
chosen_model='gemini-1.5-flash'
model = genai.GenerativeModel(chosen_model)
print("chosen_model = "+chosen_model)
# ---------------------------

def extract_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def select_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        file_name_var.set(file_path)
        # text = extract_pdf(file_path)
        # print("PDF TEXT: "+text)

def on_submit():
    # Get values from entry boxes
    title = title_entry.get()
    company = company_entry.get()
    description = description_entry.get("1.0", tk.END)
    resume = file_name_entry.get()

    if not title or not company or not description or not resume:
        message_label.config(text="Please fill all fields!")
        return
    
    message_label.config(text="Processing...")

    # Context for the "prompt" to send to Gemini
    history = [
        {
            "role" : "user",
            "parts" : [
                {
                    "text" : "The following text is from my resume: "+extract_pdf(resume)
                }
            ]
        },
        {
            "role" : "user",
            "parts" : [
                {
                    "text" : "The text that follows is a job description for a computer science related position.  Use my resume to answer the following topics.  Keep answers as short and concise as realistically possible.  Answer in bulletpoints under each topic: 1) How good of a fit is my resume with this job? 2) What skills I should add/focus on in my resume? 3) What skills I should practice for the interview."
                }
            ]
        }
    ]

    chat = model.start_chat(history=history)
    response = chat.send_message(title+" "+company+" "+" "+description)
    #print(response.text)

    # output response to file
    folder_path="output"
    file_name = os.path.join(folder_path, title+"_"+company+"_"+datetime.now().strftime("%Y-%m-%d")+".txt")
    with open(file_name, "w") as file:
        file.write(response.text)

    message_label.config(text="Outputted to file: "+file_name)

# Tkinter setup
root = tk.Tk()
root.title("Job Assistant")

file_name_var = tk.StringVar()
select_button = tk.Button(root, text="Select resume PDF file", command=select_pdf)
file_name_entry = tk.Entry(root, textvariable=file_name_var, state='readonly', width=50)

title = tk.Label(root, text="Job Title:")
title_entry = tk.Entry(root, width=50)

company = tk.Label(root, text="Company:")
company_entry = tk.Entry(root, width=50)

description = tk.Label(root, text="Job Description:")
description_entry = tk.Text(root, width=50, height=10)

submit_button = tk.Button(root, text="Submit", command=on_submit)
message_label = tk.Label(root, text="")

# Tkinter widget grid setup
select_button.grid(row=0, column=0, padx=10, pady=10)
file_name_entry.grid(row=0, column=1, padx=10, pady=10)

title.grid(row=1, column=0, padx=10, pady=5)
title_entry.grid(row=1, column=1, padx=10, pady=5)

company.grid(row=2, column=0, padx=10, pady=5)
company_entry.grid(row=2, column=1, padx=10, pady=5)

description.grid(row=3, column=0, padx=10, pady=5)
description_entry.grid(row=3, column=1, padx=10, pady=5)

submit_button.grid(row=4, column=0, columnspan=2, pady=10)
message_label.grid(row=5, column=0, columnspan=2, pady=10)

# start Tkinter loop
root.mainloop()

