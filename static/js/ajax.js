$(document).ready(function () {
    $("#search-ficha").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: function (data) {
                console.log(data)
                var html = ""
                for (var i = 0;i<data.length;i++){
                    html +='<tr><td>'+data[i].Solicitante+'</td><td>'+data[i].Empresa+'</td><td>'+data[i].AP+'</td><td>'+data[i].Evaluado+'</td><td>'+data[i].Resultado+'</td></tr>'
                }
                $('#datos').html(html);
            }

        })

    })

})

$(function () {
   var table;
   $.getJSON('')
});