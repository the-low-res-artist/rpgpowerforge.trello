# ----------------------------------
# create a venv
python3 -m venv venv
source venv/bin/activate
source /etc/rpgpowerforge/vars.ini

# ----------------------------------
# install dependencies
pip install -r requirements.txt --upgrade

# ----------------------------------
# run once
python3 main.py

# ----------------------------------
# done
deactivate