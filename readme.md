# MasseMails

## What is MasseMails ?

MasseMails is a small tool used at 404 to automate the sending of personalized attachments to a large audience.

## How to use MasseMails ?

To use MasseMails, do the following:

- Install the most recent version of Python you can find
- Install the required packages in "requirements.txt"
- Put a file named "listing.ods" on root folder. This file must contain 2 columns with, for each row, the name of the file to send and the recipient email address.
- Put the files to send on a folder (in the config.json file, is named "photos" by default. You can change this value with your own).
- Request from your admin or get a "credentials.json" file with sufficient permissions to access the Gmail API.
- Run the "main.py" file.

In the config.json file, you can edit most of the file names if needed. You can also edit the subject, body and attachment name of the emails you are about to send (an example is provided).