# AI Job Searcher

![image](https://github.com/user-attachments/assets/da857f4f-f4b1-4191-b6e6-4e2fdc072013)


## Description
A quick Python tool I put together to assist with job searching utilizing Google Gemini.

The app requires the user to input:
1) A .pdf of their resume
2) Job title
3) Company
4) Job description.

It outputs a text file with:
1) Feedback on how compatible your resume is with the job
2) Skills you should focus on in your resume
3) What skills you should focus on for the job interview.

## Dependencies
- PyPDF2
- GoogleGenerativeAI

## How to Run
1) Install dependencies
2) Get a Google API key here: https://aistudio.google.com/app/apikey
3) Set your API key as an environmental variable called "GOOGLE_API_KEY" without the quotes
4) (Optional) Switch the chosen_model variable depending on your needs and restrictions.
5) (Optional) Adjust the prompt history for your needs if necessary.
6) Run python app.py

## Planned Features
- Integration with job application website APIs
- Improve UI/UX
