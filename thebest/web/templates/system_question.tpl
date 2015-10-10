<html>
    <head>
        <title>{{ _("System Question") }}</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
        <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
    </head>
    <body>
        <script>
            $(function() {
                $("#user_answer").autocomplete({
                    source: function(request, response) {
                        var text = request.term.toLowerCase();
                        $.ajax({
                            url: "/api/suggestions?type=a&q={{ system_question }}&text=" + text,
                            type: "GET",
                            dataType: "JSON",
                            success: function(data) {
                                response($.map(data.suggestions, function(item) {
                                    return {
                                        label: item.text,
                                        id: item.text
                                    }
                                }));
                            },
                        });
                    },
                    minLength: 2
                })
            });
        </script>
        <form action="system_question" >
            <input type="hidden" name="user_question" value="{{ user_question }}" />
            <input type="hidden" name="system_question" value="{{ system_question }}" />
            <div><h2>{{ _("Answer this while we get you to the best") }} <b>{{ user_question }}.</b></h2></div>
            <div><h2>{{ _("What is for you the best") }} <b>{{ system_question }}.</b></h2></div>
            <div class="ui-widget">
                <input name="user_answer" id="user_answer">
            </div>
            <p></p>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>
