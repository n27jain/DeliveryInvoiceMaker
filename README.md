DeliveryInvoiceMaker
**Last Update:** 01/07/2021

## Description:

A web app that can store products and their details on a database and allow users to access those items to automatically create invoices and receipts in pdf format. Users can track the previous sales price and quantity used as well as have details ready in regards to use.

## How to run

1. in the app/ directory create a config.py file.*This is needed for you to host your own firebase database. In main.py from .config import config this is the imported file that contains your config parameters*
2. Copy, Paste, and fill parameters from app/config_example.py into app/config.py file then you may delete app/config_example.py
3. Create a virtual enviroment
4. Once inside the envioment run`pip3 install -r requirements.txt`*This will install all of the required packages*
5. now in the root directory you may launch the app by running`gunicorn wsgi:app`*Keep in mind gunicorn must be installed for this app to run properly on the correct port*

## Product demo :

## Purpose :

I made this app for ValueSmart Trading Inc, where regular invoices needed to be created to provide clients with price quotes and to create a receipt of all transactions done.
This app allows anyone who has no knowledge on operating word and excel to create invoices quickly and to help keep track of purchases and sales. Previously members would use a word template to manually add items to the invoice sheets but this prevents any sort of analysis opportunity which can be performed by scraping excel sheets. This app conveniently does everything using a user-friendly interface.

This app will also provide insights for yearly progression and can be used for filing revenue reports.
Since I am a shareholder of the company I made the decision to make this open-source for anyone to use and modify since many companies can benefit from this.

The overall objective for making this app was to quickly and efficiently learn python and flask to be able to host web apps for hackathons and personal projects.

## Project API's and Technologies:

- [VS Code] (IDE)
- [Python, Html, CSS] (Programing Language)
- [Firebase](https://firebase.google.com)(Database)
- [xlsxwriter](https://xlsxwriter.readthedocs.io/)](Library) used for making excel file
- [python-docx] (Library) used for making word document with details
  -[pyrebase] (Firebase Wrapper) This is a beautiful wrapper for using the Firebase API. Made queries suer easy

## Features

## Problems

- Heroku web hosting is giving us grief since v13. The current workaround is using pyinstaller to make an executable to share with the non-technical people. Regular users can simply run the code to access the website locally.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project may be used under MIT license.

