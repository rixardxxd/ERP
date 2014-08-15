function showAlert(message, priority) {
    $(document).trigger("set-alert-id-myid", [{
        'message': message,
        'priority': priority
    }]);
}

var hasOwnProperty = Object.prototype.hasOwnProperty;

function isEmpty(obj) {
    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0) return false;
    if (obj.length === 0) return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}

function getItemData(part_no, date) {
    if (part_no != null && part_no != "" && date != null && date != "") {
        var url = "/rest/item/daily/?date=" + date + "&part-no=" + part_no;
        console.log(url);
        $.getJSON(url, function(data) {
            console.log(data);
            if (isEmpty(data)) {
                showAlert("该日期此货物无发货、退货、使用信息", "warning");
            } else {
                $.each(data, function(index, value) {
                    if (value["type"] == 'U') {
                        console.log(value["amount"]);
                        $('#usage-amount-cell').html(value["amount"]);
                        showAlert("更新使用信息成功！", "success");
                    }
                    if (value["type"] == 'R') {
                        $('#return-amount-cell').html(value["amount"]);
                        showAlert("更新退货信息成功！", "success");
                    }
                    if (value["type"] == 'D') {
                        $('#delivery-amount-cell').html(value["amount"]);
                        showAlert("更新发货信息成功！", "success");
                    }

                });
            }
        }).error(function() {
            showAlert("对不起，出错了", "error")
        })
    }
}

$(document).ready(function() {
    $("#date").datepicker({
        maxDate: "+1D"
    });

    $('#part-no').click(function() {
        $('.modal-body').load('/products/', function(result) {
            $('#myModal').modal({
                show: true
            });
        });
    });

    var modal = $('#myModal');


    // Filter clicks within the modal to those on the save button (#submit-modal)
    modal.on('click', '#save-modal', function(e) {
        var placeholder = "";
        $(".selected").each(function(index, value) {
            var part_no = $(this).find(".part-no").text();
            console.log(part_no);
            if (part_no.length) {
                $('#part-no').val(part_no);
                placeholder = part_no;
            }
        });
        console.log(placeholder);
        $('.part-no-cell').html(placeholder);
        getItemData($('#part-no').val(), $('#date').val());

    });



    $('.alert .close').on('click', function(e) {
        $(this).parent().hide();
    });


});