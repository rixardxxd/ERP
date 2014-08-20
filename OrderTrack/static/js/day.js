
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
            var usage_flag = false;
            var delivery_flag = false;
            var return_flag = false;
            //clear previous amount
            $('#usage-amount-input').val("");
            $('#return-amount-input').val("");
            $('#delivery-amount-input').val("");
            if (isEmpty(data)) {
                showAlert("该日期此货物无发货、退货、使用信息", "warning");
            } else {
                $.each(data, function(index, value) {
                    if (value["type"] == 'U') {
                        console.log(value["amount"]);
                        $('#usage-amount-input').val(value["amount"]);
                        showAlert("获取使用信息成功！", "success");
                        usage_flag = true;
                    }
                    if (value["type"] == 'R') {
                        $('#return-amount-input').val(value["amount"]);
                        showAlert("获取退货信息成功！", "success");
                        return_flag = true;
                    }
                    if (value["type"] == 'D') {
                        $('#delivery-amount-input').val(value["amount"]);
                        showAlert("获取发货信息成功！", "success");
                        delivery_flag = true;
                    }
                });
            }

            if (usage_flag) {
                enableUpdateAndDeleteButton("usage");
            } else {
                enableAddButton("usage");
            }

            if (return_flag) {
                enableUpdateAndDeleteButton("return");
            } else {
                enableAddButton("return");
            }

            if (delivery_flag) {
                enableUpdateAndDeleteButton("delivery");
            } else {
                enableAddButton("delivery");
            }

        }).error(function() {
            showAlert("对不起，出错了", "error")
        })
    }
}

function enableAddButton(type) {
    var add_button = "#" + type + "-add-button";
    $(add_button).removeAttr('disabled');
    var update_button = "#" + type + "-update-button";
    var delete_button = "#" + type + "-delete-button";
    $(update_button).attr('disabled', 'disabled');
    $(delete_button).attr('disabled', 'disabled');
}

function enableUpdateAndDeleteButton(type) {
    var update_button = "#" + type + "-update-button";
    var delete_button = "#" + type + "-delete-button";
    $(update_button).removeAttr('disabled');
    $(delete_button).removeAttr('disabled');
    var add_button = "#" + type + "-add-button";
    $(add_button).attr('disabled', 'disabled');
}

function addItem(type) {
    var data = validatePostData(type);
    if(data == null){
        return;
    }
    makeAjaxPOST("/rest/item/add/", data, "add", type);

}

function updateItem(type) {
    var data = validatePostData(type);
    if(data == null){
        return;
    }
    makeAjaxPOST("/rest/item/update/", data, "update", type);
}

function deleteItem(type) {
    var data = validatePostData(type);
    if(data == null){
        return;
    }
    makeAjaxPOST("/rest/item/delete/", data, "delete", type);
}

function makeAjaxPOST(url, data, operation, type) {
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        },
        success: function(data, textStatus, xhr) {
            showAlert("操作成功！", "success");
            if(operation == "add"){
                enableUpdateAndDeleteButton(type);
            }
            if(operation == "update"){
                enableUpdateAndDeleteButton(type);
            }
            if(operation == "delete"){
                enableAddButton(type);
                $('#' + type + '-amount-input').val("");
            }

        },
        error: function(xhr, textStatus, errorThrown) {
            showAlert("操作失败！", "error");
        }
    });
}

function validatePostData(type) {
    var part_no = $(".part-no-cell").html();
    console.log(part_no);
    if (part_no == null || part_no.length == 0) {
        showAlert("缺少Part No信息！", "error");
        return null;
    }
    var date = $('#date').val();
    if (date == null || date.length == 0) {
        showAlert("缺少日期信息！", "error");
        return null;
    }
    var amount = $('#' + type + '-amount-input').val();
    if (amount == null || amount <= 0) {
        showAlert("缺少数量信息！", "error");
        return null;
    }
    var data = new Object();
    data.part_no = part_no;
    data.date = date;
    data.amount = amount;
    data.type = type;
    return data;
}

$(document).ready(function() {
    var datepiackerOptions = {
        maxDate: "+1D",
        onClose: function() {
            var part_no = $("#part-no").val();
            console.log(part_no);
            if (part_no != null && part_no.length) {
                getItemData($('#part-no').val(), $(this).val());
            }
        }
    }
    $("#date").datepicker(datepiackerOptions);

    $('#part-no').click(function() {
        $('#product-modal .modal-body').load('/products/', function(result) {
            $('#product-modal').modal({
                show: true
            });
        });
    });

    var modal = $('#product-modal');

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

    $("#delivery-delete-button,#return-delete-button,#usage-delete-button").click(function(){
        var type=$(this).data('type');
        console.log(type);
        $("#delete-confirmation-modal .hidden-input").val(type);

    });

    $("#delete-confirmation-button").click(function(){
        var type = $("#delete-confirmation-modal .hidden-input").val();
        if (type == null || type.length == 0){
            showAlert("错误！无法删除该数据！", "error");
            return;
        }
        deleteItem(type);

    });


});