import email
import configparser
import imaplib

# laduje hasla i delikatne dane
config = configparser.ConfigParser()
config.read('settings.ini')

#dane logowania email
wysylki_adres = config.get('email','adres_mail')
wysylki_pass = config.get('email','pass')

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.asgard.gifts")
# authenticate
imap.login(wysylki_adres, wysylki_pass)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 50
# total number of emails
messages = int(messages[0])
print(messages)

for i in range(messages, messages-N, -1):
  msg_body = ''
  # fetch the email message by ID
  try:
      res, msg = imap.fetch(str(i), "(RFC822)")
  except:
      print('niemoglem odczytać maila')
      break
  czy_sprawdzac_mail = 1
  for response in msg:        
      if isinstance(response, tuple):
          print('*')
          # parse a bytes email into a message object
          msg = email.message_from_bytes(response[1])
          # decode the email subject
          subject, encoding = email.header.decode_header(msg["Subject"])[0]
          if isinstance(subject, bytes):
              # if it's a bytes, decode to str
              subject = subject.decode(encoding).strip()
          # decode email sender
          From, encoding = email.header.decode_header(msg.get("From"))[0]
          if isinstance(From, bytes):
              From = From.decode(encoding).strip()

          if From == 'infoagent@dpd.com.pl': #and subject == 'Raport DPD Polska':
              print('MAM maila od DPD')
              #czy_sprawdzac_mail = 0
              #break            
          print("="*100)
          print("Subject:", subject)
          print("From:", From)
          # if the email message is multipart
          if msg.is_multipart():
              # iterate over email parts
              for part in msg.walk():
                  # extract content type of email
                  content_type = part.get_content_type()
                  content_disposition = str(part.get("Content-Disposition"))
                  try:
                      # get the email body
                      msg_body = part.get_payload(decode=True).decode()
                  except:
                      pass
          else:
              # extract content type of email
              content_type = msg.get_content_type()
              # get the email body
              msg_body = msg.get_payload(decode=True).decode()
          #print(body)
