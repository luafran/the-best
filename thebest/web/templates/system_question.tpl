<html>
    <head>
        <title>{{ _("System Question") }}</title>
    </head>
    <body>
        <form action="user_answer" >
            <input type="hidden" name="user_item" value="{{ user_item }}" />
            <div>{{ _("What is for you the best") }} {{ system_item }}</div>
            <div><input type="text" name="user_text"/></div>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
