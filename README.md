installeren al of niet met virtual env
zie requirements.txt
eventueel: pip install -r requirements.txt
jquery nodig (angular niet)
met bower installeren
(index.html rekent erop, ik bedoel _base.html)

    <script src="{% static 'bower_components/jquery/dist/jquery.js' %}"></script>
    <script src="{% static 'bower_components/typeahead.js/dist/typeahead.jquery.min.js' %}"></script>
    <script src="{% static 'bower_components/typeahead.js/dist/bloodhound.min.js' %}"></script>

in terminal
cd website/static
nvm use 5 (vermijd het probleem met de tryModuleLoad exceptie)
bower install jquery 
bower install typeahead.js
nvm use 9
