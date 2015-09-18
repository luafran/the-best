<html>
    <head>
        <title>{{ _("First Time Question!") }}</title>
    </head>
    <body>
        <form action="/" >
            <input type="hidden" name="user_question" value="{{ user_question }}" />
            <div><h1>{{ _("Wow! This is the first time somebody ask for the best") }} <b>{{ user_question }}.</b></h1></div>
            <div><h1>{{ _("Congrats!") }}</h1></div>
            <div><h2>{{ _("We will try to find an answer soon") }}.</h2></div>
            <div><input type="submit" value="{{ _("Got it") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
