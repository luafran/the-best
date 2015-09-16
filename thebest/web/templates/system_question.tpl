<html>
    <head>
        <title>{{ _("System Question") }}</title>
    </head>
    <body>
        <form action="user_answer" >
            <input type="hidden" name="user_category" value="{{ user_category }}" />
            <div>{{ _("Answer this while we get you to the best") }} <b>{{ user_category }}</b></div>
            <div>{{ _("What is for you the best") }} <b>{{ system_category }}</b></div>
            <div><input type="text" name="user_text"/></div>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
