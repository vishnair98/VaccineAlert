# VaccineAlert
Python based approach to notify user on open vaccination slots
This project was solely done for learning purposes, and for a use case scenario where vaccine slots would be booked within 10 minutes of availibility. This script
notifies the user through a mail, when the next dose is available, thus reducing wait.

Important Notes:

1. The code runs on Python 2.7
2. Have an SMTP Server up and running on your shell. The command-line for this is included in the code as well.
3. Before running the script, make sure your account settings to accept mails from less-reliable sources is turned on.
4. The idea is to send a notification, only if slots are available. Add this condition through (dose1 or dose2 > 0) for specific use case.
