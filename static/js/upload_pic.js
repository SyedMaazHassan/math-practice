function upload_file(whick_input) {
    $("#"+whick_input).click();
}

function readURL(input, show) {
    $("#"+show).css('display', 'none');
    nameFile = input.files[0].name.split(".");
    nameFile = nameFile[nameFile.length-1];
    
    console.log(nameFile);
    if(nameFile=="png" || nameFile=="jpg" || nameFile=="jpeg" || "JPG"){
        if (input.files && input.files[0]) {
            $("#file-error-msg").text("");

            var reader = new FileReader();

            // if (nameFile == "docx") {
            //     show = show+"_2";
            // }

            reader.onload = function (e) {
                var result_to_show = e.target.result;
                console.log(result_to_show)
                $("#"+show).css('display', '');
                $("#"+show).prop("class", "decrease-s-width");
                $('#'+show)
                    .attr('src', result_to_show)
                    .width('90px')
                    .height('90px');

                // $("#preview").modal("show");
                $("#showing_div").show();
                $("#image_error").hide();
            };

            if (!(nameFile == "docx" || nameFile == "doc")) {
                $("#see_docs_file").css('display', 'none');
                reader.readAsDataURL(input.files[0]);
            }else{
                $("#see_docs_file").css('display', '');
                reader.readAsDataURL(input.files[0]);
            }

            $("#success-msg").css('display', '');

        }
    }else{
        $("#target_file").val(null);    
        $("showing_div").removeClass("dragover");
        $("#showing_div").hide();
        $("#image_error").show();

    }

}


