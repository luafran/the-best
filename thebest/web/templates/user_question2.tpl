<html>
<head>
    <link rel="stylesheet" href="/examples/stylesheets/ui-lightness/jquery-ui-1.8.16.custom.css" type="css">
    <script type="text/javascript" src="/static/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/static/jquery-ui.min.js"></script>
</head>

<body>
<script>
    $(function() {
        $("#keyword").autocomplete({
            source: function(request, response) {
                var prefix = { "name": request.term.toLowerCase() };
                var postData = {
                    "query": { "prefix": prefix },
                    "fields": ["name", "_id"]
                };
                $.ajax({
                    url: "http://localhost:9200/the-best-test/category/_search",
                    type: "GET",
                    dataType: "JSON",
                    data: JSON.stringify(postData),
                    success: function(data) {
                        response($.map(data.hits.hits, function(item) {
                            return {
                                label: item._source.name,
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
