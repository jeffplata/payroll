REM set this in the working folder
REM FLASK_APP should be 0, debug off
set MAIL_SERVER=localhost
set MAIL_PORT=8025

REM run this in a different shell
python -m smtpd -n -c DebuggingServer localhost:8025
