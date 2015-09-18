<html>
    <head>
        <title>{{ _("System Question") }}</title>
    </head>
    <body>
        <form action="system_question" >
            <input type="hidden" name="user_question" value="{{ user_question }}" />
            <div><h2>{{ _("Answer this while we get you to the best") }} <b>{{ user_question }}.</b></h2></div>
            <div><h2>{{ _("What is for you the best") }} <b>{{ system_question }}.</b></h2></div>
            <div><input type="text" name="user_text"/></div>
            <p></p>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
