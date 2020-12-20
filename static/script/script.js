$(function(){
    $("#instructionButton").click(function(){
        $("#instructionmodal").modal("show");
    });
    $('#upload').on('change', function () {
        readURL(input);
    });

    $('#recognize').click(function(){
        if(image){
            $('#resultImg')
                .attr('src', image);  
        }
        else{
            $('#imgError').removeClass('fade');
        }
        
    });
    $('#model_name').change(showResult);
    showM();
});
function showM(){
    console.log($("#showM").text().replace(/^\s+|\s+$/g,''))
    console.log($("#showM").text().replace(/^\s+|\s+$/g,'') == '');
    if(!($("#showM").text().replace(/^\s+|\s+$/g,'') == '')){
        $("#resultmodal").modal('show');
    }

}
var image;
console.log(image)
var alpha =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imgError').addClass('fade');
            $('#imageResult')
                .attr('src', e.target.result);
            image = e.target.result;
            $('#upload-label').text(input.files[0].name)
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function showResult(){
var value = $('#model_name option:selected').attr('value');
$("#prediction").empty();
$("#prediction").append(`<h1>${value}</h1>`);
}