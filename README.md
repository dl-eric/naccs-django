# NACCS website
![](https://img.shields.io/website/https/www.collegiatecounterstrike.com.svg)

This is the official repository for the North American Collegiate Counter-Strike website!

Master branch should ALWAYS be production ready. No continuous deployment is set up at the moment.

## Local Deployment

Once you have your variables set up, move on.

*We are using a virtual environment to contain our dependencies.

Linux:
Clone the repository and go into the root folder.

```
# In Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd naccsweb/
python manage.py runserver
```
