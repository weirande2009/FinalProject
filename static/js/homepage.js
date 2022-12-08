
let image = '';

function inputImage(fileDOM){
    var file = fileDOM.files[0],
        imageType = /^image\//,
        reader = '';

    if(!imageType.test(file.type)){
        alert("Please select an image");
        return;
    }

    if(window.FileReader){
        reader = new FileReader();
    }
    else{
        alert("Please update your browser!")
        return;
    }

    reader.onload = function (evt){
        document.getElementById("label").style.display = "none"
        $('#image').attr("src", evt.target.result);
        image = evt.target.result;
    }

    reader.readAsDataURL(file)
}

var options={
        success : showResponse,    // callback function
        timeout : 3000
    }

var submitChange = function(){
        $("#form_submit").ajaxSubmit(options);
        return false;
    };

function showResponse(responseText, statusText){
    if(statusText !== "success"){
        alert("Error!!!")
    }
    else{
        document.getElementById("label").style.display = "block"
        $("#label").html("Analysis Result: "+responseText.name);
    }
}
