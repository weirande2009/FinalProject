sudo apt update
sudo apt -y install python3-pip
python3 -m pip install virtualenv
python3 -m virtualenv django
source django/bin/activate
pip install django opencv-python-headless
cd django
git clone https://github.com/weirande2009/FinalProject.git
cd FinalProject
python manage.py makemigrations
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:8080


