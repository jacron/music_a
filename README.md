#Python
installeren al of niet met virtual env

zie requirements.txt

eventueel: pip install -r requirements.txt

#Port
client luister-muziek-a rekent op 8010

configureren in edit run configurations in Pycharm

#Javascript
_base.html

    <script src="{% static 'bower_components/jquery/dist/jquery.js' %}"></script>
    <script src="{% static 'bower_components/typeahead.js/dist/typeahead.jquery.min.js' %}"></script>
    <script src="{% static 'bower_components/typeahead.js/dist/bloodhound.min.js' %}"></script>

in terminal

    cd website/static
    nvm use 5 (vermijd het probleem met de tryModuleLoad exceptie)
    bower install jquery 
    bower install typeahead.js
    nvm use 9

#redis
channels heeft redis nodig

#windows
pip install pypiwin32

#bower
nvm use 5.11

npm i bower

bower install

jquery, typeahead, bloodhound

git config --global url."git://".insteadOf https://
git config --global --unset url.git://.insteadof


#run
python ./manage.py runserver 8010
