<html>
    <head>
        <title>{{ _("User Question") }}</title>
    </head>
    <body>
        <form action="system_question" >
            <div class="groupMenu">
                {{ _("Tell me please the best ") }}
                <select name="item" id="groupDropDown">
                {% for item in items %}
                    <option value="{{ item }}">{{ item }}</option>
                {% end %}
                </select>
            </div>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
