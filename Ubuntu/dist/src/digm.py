import sys
import imaplib
import getpass
import email
import email.header
import datetime
import os
import re
import smtplib

detach_dir = "."
EMAIL_ACCOUNT = ""
EMAIL_FOLDER = ""
EMAIL_PASS = ""
list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def prompt(prompt):
    return raw_input(prompt).strip()


def sendmail(EMAIL_ACCOUNT, EMAIL_PASS, M):
    fromaddr = prompt("From: ")
    toaddrs  = prompt("To: ").split()
    print "Enter message, end with ^D :"

    msg = ("From: %s\r\nTo: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs)))
    while 1:
        try:
            line = raw_input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ACCOUNT,EMAIL_PASS)
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    major(EMAIL_ACCOUNT, EMAIL_PASS, M)




def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)




def get_mailbox(EMAIL_ACCOUNT, EMAIL_PASS,  M,  EMAIL_FOLDER):
    
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    if(os.path.exists("../../MAIL/"+EMAIL_FOLDER)):
        print "Folder Exists"
    else:
        os.makedirs("../../MAIL/"+EMAIL_FOLDER)
    detach_dir="../../MAIL/"+EMAIL_FOLDER+"/"
    att_path1 = os.path.join(detach_dir, EMAIL_FOLDER+".txt")
    fplog = open(att_path1, 'wb')

    
    #os.makedirs(EMAIL_FOLDER+"/MAILS")
 
    for num in data[0].split():
        if(os.path.exists("../../MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num)):
            print "Folder Exists"
        else:
            os.makedirs("../../MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num)
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        msg = email.message_from_string(data[0][1])
        xyz = msg
        body = "OOPS!! No Body"
        if xyz.get_content_maintype() == 'multipart': 
            for part in xyz.walk():       
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
        else:
            for part in xyz.walk():
                body = part.get_payload(decode=True)
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        filename = EMAIL_FOLDER+num+".txt"
        detach_dir="../../MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num+"/"
        att_path = os.path.join(detach_dir, filename)
        
        print ("Accessing..")
        fp = open(att_path, 'wb')

        fp.write("Subject : ")
        fp.write(subject)
        fp.write("\nDate : ")
        fp.write( msg['Date'])
        fp.write("\nFrom : ")
        fp.write( msg['From'])
        fp.write("\n\nMessage : \n")
        fp.write( body)

        fplog.write("MAIL : "+num)
        fplog.write("\nSubject : ")
        fplog.write(subject)
        fplog.write("\nDate : ")
        fplog.write( msg['Date'])
        fplog.write("\nFrom : ")
        fplog.write( msg['From'])
        fplog.write("\n\nMessage : \n")
        fplog.write( body)
        
        xyz = msg

        fp.write("\n\nAttachments : \n")
        fplog.write("\n\nAttachments : \n")

        if xyz.get_content_maintype() == 'multipart': 
            for part in xyz.walk():      
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True) 

                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                counter = 1

                if not filename:
                    filename = 'part-%03d%s' % (counter, 'bin')
                    counter += 1
                #detach_dir=EMAIL_FOLDER+"/"
                att_path = os.path.join(detach_dir, filename)
                fp.write(filename)
                fp.write("\n")

                fplog.write(filename)
                fplog.write("\n")

                if not os.path.isfile(att_path) :
                    fpc = open(att_path, 'wb')
                    fpc.write(part.get_payload(decode=True))
                    fpc.close()

        fp.close()
        fplog.write("\n\n-----------------------------------------END--------------------------------------------------------------------------\n\n")
    fplog.close()

    major(EMAIL_ACCOUNT, EMAIL_PASS, M)



def access_mailbox(EMAIL_ACCOUNT, EMAIL_PASS,  M,  EMAIL_FOLDER):
    
    rv, data = M.search(None, "UNSEEN")
    if rv != 'OK':
        print "No messages found!"
        return
    if(os.path.exists("../../UNREAD_MAIL/"+EMAIL_FOLDER)):
        print "Folder Exists"
    else:
        os.makedirs("../../UNREAD_MAIL/"+EMAIL_FOLDER)
    detach_dir="../../UNREAD_MAIL/"+EMAIL_FOLDER+"/"
    att_path1 = os.path.join(detach_dir, EMAIL_FOLDER+".txt")
    fplog = open(att_path1, 'wb')

    
    #os.makedirs(EMAIL_FOLDER+"/MAILS")
 
    for num in data[0].split():
        if(os.path.exists("../../UNREAD_MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num)):
            print "Folder Exists"
        else:
            os.makedirs("../../UNREAD_MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num)
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        msg = email.message_from_string(data[0][1])
        xyz = msg
        body = "OOPS!! No Body"
        if xyz.get_content_maintype() == 'multipart': 
            for part in xyz.walk():       
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
        else:
            for part in xyz.walk():
                body = part.get_payload(decode=True)
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        filename = EMAIL_FOLDER+num+".txt"
        detach_dir="../../UNREAD_MAIL/"+EMAIL_FOLDER+"/"+EMAIL_FOLDER+num+"/"
        att_path = os.path.join(detach_dir, filename)
        
        print ("Accessing..")
        fp = open(att_path, 'wb')

        fp.write("Subject : ")
        fp.write(subject)
        fp.write("\nDate : ")
        fp.write( msg['Date'])
        fp.write("\nFrom : ")
        fp.write( msg['From'])
        fp.write("\n\nMessage : \n")
        fp.write( body)

        fplog.write("MAIL : "+num)
        fplog.write("\nSubject : ")
        fplog.write(subject)
        fplog.write("\nDate : ")
        fplog.write( msg['Date'])
        fplog.write("\nFrom : ")
        fplog.write( msg['From'])
        fplog.write("\n\nMessage : \n")
        fplog.write( body)
        
        xyz = msg

        fp.write("\n\nAttachments : \n")
        fplog.write("\n\nAttachments : \n")

        if xyz.get_content_maintype() == 'multipart': 
            for part in xyz.walk():      
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True) 

                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                counter = 1

                if not filename:
                    filename = 'part-%03d%s' % (counter, 'bin')
                    counter += 1
                #detach_dir=EMAIL_FOLDER+"/"
                att_path = os.path.join(detach_dir, filename)
                fp.write(filename)
                fp.write("\n")

                fplog.write(filename)
                fplog.write("\n")

                if not os.path.isfile(att_path) :
                    fpc = open(att_path, 'wb')
                    fpc.write(part.get_payload(decode=True))
                    fpc.close()

        fp.close()
        fplog.write("\n\n-----------------------------------------END--------------------------------------------------------------------------\n\n")
    fplog.close()

    major(EMAIL_ACCOUNT, EMAIL_PASS, M)



def main():

    print("###########################################################################")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                   Welcome to the DIGM :V-1.0.0                          #")
    print("#                     By - Asim Krishna Prasad                            #")
    print("#                    http://github.com/pakhandi                           #")
    print("#                       http://bugecode.com                               #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("###########################################################################")
    print ""
    print ""
    print("Connecting to Gmail .. .. ")
    M = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        EMAIL_ACCOUNT = prompt("Username : ")
        EMAIL_PASS = getpass.getpass()
        rv, data = M.login(EMAIL_ACCOUNT,EMAIL_PASS)
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!!! "
        sys.exit(1)

    print rv, data

    major(EMAIL_ACCOUNT,EMAIL_PASS, M)

def major(EMAIL_ACCOUNT, EMAIL_PASS, M):
    print("\n\n\n################################")
    print("MENU : ")
    print("1: Sync Mail-Boxes")
    print("2: Send a Mail")
    print("3: Check Mail-Box")
    print("4: EXIT")
    print("Enter your choice : \n\n")

    dec = raw_input()

    if dec == '4':
        sys.exit(0);

    if dec == '1':
        
        rv, mailboxes = M.list()
        if rv == 'OK':
            print "Mailboxes:"
            for line in mailboxes:
                print 'Server response:', line
                flags, delimiter, mailbox_name = parse_list_response(line)
                #print 'Parsed response:', (flags, delimiter, mailbox_name)

        print "Enter the mail-folder you want to sync : "
        EMAIL_FOLDER = raw_input();
         
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            print "Getting mailbox...\n"
            get_mailbox(EMAIL_ACCOUNT, EMAIL_PASS, M, EMAIL_FOLDER)
            M.close()
        else:
            print "ERROR: Unable to open mailbox ", rv

    if dec == '3':
        
        rv, mailboxes = M.list()
        if rv == 'OK':
            print "Mailboxes:"
            for line in mailboxes:
                print 'Server response:', line
                flags, delimiter, mailbox_name = parse_list_response(line)

        print "Enter the mail-folder you want to read : "
        EMAIL_FOLDER = raw_input();
         
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            print "Reading mailbox...\n"
            access_mailbox(EMAIL_ACCOUNT, EMAIL_PASS,  M, EMAIL_FOLDER)
            M.close()
        else:
            print "ERROR: Unable to open mailbox ", rv

    if dec == '2':
        sendmail(EMAIL_ACCOUNT, EMAIL_PASS, M)

    else:
        print "Wrong Selection"
        major(EMAIL_ACCOUNT,EMAIL_PASS, M)


     
    M.logout()

if __name__ == "__main__":
    main()
