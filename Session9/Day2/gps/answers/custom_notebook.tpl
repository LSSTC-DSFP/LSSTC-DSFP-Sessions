{% extends 'null.tpl'%}

{%- block body %}
{{ nb | json_dumps }}
{% endblock body %}