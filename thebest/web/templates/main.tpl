<html>
    <head>
        <title>{{ _("User Question") }}</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
        <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
    </head>
    <body>
        <script>
            $(function() {
                $("#user_question").autocomplete({
                    source: function(request, response) {
                        var text = request.term.toLowerCase();
                        $.ajax({
                            url: "/api/suggestions/question?text=" + text,
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
        <form action="user_question" >
            <div class="groupMenu">
                <div class="ui-widget">
                    {{ _("Tell me please the best ") }} <input name="user_question" id="user_question">
                </div>
            </div>
            <div><input type="submit" value="{{ _("Go") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>