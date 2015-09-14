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
                $("#category").autocomplete({
                    source: function(request, response) {
                        var prefix = request.term.toLowerCase();
                        $.ajax({
                            url: "/category/suggestions?prefix=" + prefix,
                            type: "GET",
                            dataType: "JSON",
                            success: function(data) {
                                response($.map(data.suggestions, function(item) {
                                    return {
                                        label: item.name,
                                        id: item._id
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
            <div class="groupMenu">
                {{ _("Tell me please the best ") }}
                <div class="ui-widget">
                    <input name="category" id="category">
                </div>
            </div>
            <div><input type="submit" value="{{ _("Tell me please") }}"/></div>
        {% module xsrf_form_html() %}
        </form>
    </body>
</html>