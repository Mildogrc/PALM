(function ($) {

    var handleFileSelect = function (evt) {
        var files = evt.target.files;
        var file = files[0];

        if (files && file) {
            var reader = new FileReader();

            reader.onload = function (readerEvt) {
                var binaryString = readerEvt.target.result;
                document.getElementById("base64textarea").value = btoa(binaryString);
                //$("shownimage").attr('src', readertarget.result);

            };

            reader.readAsBinaryString(file);
            //document.getElementById("shownimage").hidden=false;
        }
    };

    if (window.File && window.FileReader && window.FileList && window.Blob) {
        document.getElementById('filePicker').addEventListener('change', handleFileSelect, false);
    } else {
        alert('The File APIs are not fully supported in this browser.');
    }

    $("#predict-button").click(function (event) {
        if (checkFile()) {
            document.getElementById("loadingmodel").showModal();
            document.getElementById("predict-button").hidden = true;
            document.getElementById("loading-button").hidden = false;
            document.getElementById("loadingimage").hidden = false;
            let base64Image = document.getElementById("base64textarea").value;
            let message = {
                image: base64Image
            }
            console.log(message);
            $.post("/predict", JSON.stringify(message), function (response) {
                document.getElementById("loadingmodel").close();
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#gifstop").offset().top
                }, 2000);
                document.getElementById("loadingimage").hidden = true;
                document.getElementById("loading-button").hidden = true;
                var probOfPneumonia = response.prediction.prob;
                var filepath = response.prediction.filepath;
                var stringofchance = "";
                if (probOfPneumonia < 20) {
                    stringofchance = "low"
                    $("#Pneumonia-predict").text(probOfPneumonia);
                    $("#Pneumonia-predict-low").text(stringofchance);
                    document.getElementById("Pneumonia-predict").hidden = false;
                    document.getElementById("highchance").hidden = true;
                    document.getElementById("mildchance").hidden = true;
                    document.getElementById("lowchance").hidden = false;
                    document.getElementById("shownimage").hidden = false;
                    if (probOfPneumonia = 0) {
                        document.getElementById("shownimage").hidden = true;
                    }
                } else {
                    if (probOfPneumonia < 80) {
                        stringofchance = "medium(not well known)";
                        $("#Pneumonia-predict").text(probOfPneumonia);
                        $("#Pneumonia-predict-medium").text(stringofchance);
                        document.getElementById("mediumDialog").showModal();
                        document.getElementById("lowchance").hidden = true;
                        document.getElementById("highchance").hidden = true;
                        document.getElementById("mildchance").hidden = true;

                    } else {
                        stringofchance = "high";
                        $("#Pneumonia-predict").text(probOfPneumonia);
                        $("#Pneumonia-predict-high").text(stringofchance);
                        document.getElementById("highDialog").showModal();
                        document.getElementById("lowchance").hidden = true;
                        document.getElementById("mildchance").hidden = true;
                        document.getElementById("highchance").hidden = true;
                    }
                }
                document.getElementById("shownimage").src = filepath;
                //document.getElementById("shownimage1").hidden=true;
                //document.getElementById("shownimage2").hidden=false;
            });
        }
    });


    $("#highhide").click(function (event) {
        document.getElementById("highDialog").close();
        document.getElementById("highchance").hidden = false;
        document.getElementById("Pneumonia-predict").hidden = false;
        document.getElementById("shownimage").hidden = false;
    });


    $("#mediumhide").click(function (event) {
        document.getElementById("mediumDialog").close();
        document.getElementById("mildchance").hidden = false;
        document.getElementById("Pneumonia-predict").hidden = false;
        document.getElementById("shownimage").hidden = false;
    });


    $("input[type=file]").change(function () {
        document.getElementById("noresume").hidden=true;
        document.getElementById("badresume").hidden=true;
        var fieldVal = $(this).val();
        document.getElementById("predict-button").hidden = false;
        document.getElementById("shownimage").hidden = true;
        document.getElementById("lowchance").hidden = true;
        document.getElementById("mildchance").hidden = true;
        document.getElementById("highchance").hidden = true;
        document.getElementById("Pneumonia-predict").hidden = true;
        // Change the node's value by removing the fake path (Chrome)
        var fieldValDisplay = fieldVal.replace("C:\\fakepath\\", "");
        // var path = "Images/" + fieldValDisplay;
        var path = fieldValDisplay;
        // document.getElementById("shownimage").src="faearioafe";
        document.getElementById("filePicker").src = path;
        console.log
        if (fieldValDisplay != undefined || fieldValDisplay != "") {
            $(this).next(".custom-file-label").attr('data-content', fieldValDisplay);
            $(this).next(".custom-file-label").text(fieldValDisplay);
        }
        //document.getElementById("shownimage").src=temp.jpg;
        //document.getElementById("shownimage").hidden=false;
    });

    function checkFile() {
        var fileElement = document.getElementById("filePicker");
        if (fileElement.src.length == 0) {
            document.getElementById("noresume").hidden = false;
            return false;
        } else {
            var fileExtension = "";
            if (fileElement.value.lastIndexOf(".") > 0) {
                fileExtension = fileElement.value.substring(fileElement.value.lastIndexOf(".") + 1, fileElement.value.length);
            }
            if (fileExtension.toLowerCase() == "jpg" |
                fileExtension.toLowerCase() == "png" |
                fileExtension.toLowerCase() == "gif" |
                fileExtension.toLowerCase() == "jpeg") {
                return true;
            }
            else {
                document.getElementById("badresume").hidden = false;
                return false;
            }
        }
    }
})(jQuery);