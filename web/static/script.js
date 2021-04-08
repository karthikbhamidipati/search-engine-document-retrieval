        $("#input").keyup(function () {
            var text = $(this).val();
            $.ajax({
                url: "/suggestions",
                type: "get",
                data: {search_query: text},
                success: function (response) {
                    $("#suggestions").html(response);
                },
                error: function (xhr, exception) {
                    $('#post').html(xhr.status + ' ' + exception.message);
                }
            });
        });
