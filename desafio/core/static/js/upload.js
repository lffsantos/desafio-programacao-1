$(document).ready(function() {
    $("form").submit(function () {
        var name_file = $("#id_file").val().split('\\');
        if(name_file == ""){
            alert("É necessário informar um arquivo para upload!")
            event.preventDefault();
            return
        }
    });
});