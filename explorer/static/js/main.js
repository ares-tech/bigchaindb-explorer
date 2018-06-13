var apiBaseUrl = window.location.protocol + "//" + window.location.host;

var apiDataType = "json";
var apiExtraHeaders = {"X-Api-Key": "4102ff70258262791567b83c327d61c53db60da48128184af53268b17c769ba4",
                       "Content-Type": "application/json"};

jQuery(function($) {
    var makeCall = function(apiUrl, apiExtraHeaders) {
        // show spinnner
        $('#loading').show();

        $.ajax({
            url : apiUrl,
            type: "GET",
            dataType : "json",
            headers : apiExtraHeaders
        }).success(function(data, textStatus, jqXHR) {
            if (data) {
                $.JSONView(data, $('#result'));
            } else {
                $.JSONView({}, $('#result'));
                $('#result').html('<ol><li>Server returned no data. (HTTP Status Code: ' + jqXHR.status + ' – ' + jqXHR.statusText + ')</li></ol>'); // 204 for example
            }
            $('#loading').hide();
        }).error(function(jqXHR, textStatus, errorThrown) {
            $.JSONView(jqXHR.responseText ? JSON.parse(jqXHR.responseText) : {}, $('#result'));
            $('#loading').hide();
        });
    };

    // hook sidebar clicks
    $('#sidebar').on('click', 'a', function(e, dontpush) {
        e.preventDefault();
        if ($('#loading').is(':hidden')) {
            $('#sidebar a').removeClass('active');
            $(this).addClass('active');
            var url = $(this).attr('href');
            var requestmethod = $(this).data('requestmethod').toLowerCase() || 'get';
            $('#apiurl').val(apiBaseUrl + url);
            makeCall(apiBaseUrl + url, apiExtraHeaders);
        }
    });

    // hook form submit
    $('form').on('submit', function(e, dontpush){
        e.preventDefault();
        if ($('#apiurl').val().indexOf(apiBaseUrl) == 0) {
            var url = $('#apiurl').val().replace(apiBaseUrl,'');
            var method = $('#requestmethod').val().toLowerCase();
            $('#sidebar a').removeClass('active');
            $('#sidebar a').attr('href', url);
            $('#sidebar a').attr('data-requestmethod', method);
            $('#sidebar a').addClass('active');
            makeCall(apiBaseUrl + url, apiExtraHeaders);
        } else {
            alert('You are only allowed make calls to ' + apiBaseUrl);
        }
    });

    $('#sidebar a:first').addClass('active').trigger('click', true);

});
