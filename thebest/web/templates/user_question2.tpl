<html>
<head>
    <script type="text/javascript" src="/static/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/static/jquery-ui.min.js"></script>
</head>

<body>
<script>
    $(function() {
        $("#keyword").autocomplete({
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


<div class="demo">
    <h1>Autocomplete using cross origin resource sharing with elasticsearch</h1>
    <br>

    <div class="ui-widget">
        <label for="keyword">Keyword: </label>
        <input id="keyword">
    </div>


</body>
</html>
