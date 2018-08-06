import smtplib


def send(username, password, target, msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.connect('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)

	for email in target:
		server.sendmail(username, email, msg)
	server.quit()