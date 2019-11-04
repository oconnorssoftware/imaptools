import sys,json
import imaplib
import email

credConfig = dict()
with open("mailcreds.json",'r') as fh:
    credConfig = json.loads(fh.read())

M = imaplib.IMAP4_SSL('imap.gmail.com',993)
M.login(credConfig["username"], credConfig["password"])

M.select('Inbox')
type, data = M.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)' )
    raw_email = data[0][1]

    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    print(email_message)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # downloading attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join('./', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
