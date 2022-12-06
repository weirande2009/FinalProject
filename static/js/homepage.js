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
        $('#image').attr("src", evt.target.result);
        image = evt.target.result;
    }

    reader.readAsDataURL(file)
}

function uploadImage(){
    $.post("/recognize/",
        {image: image},
        function (data){
            $("#label").html(data.name);
        })
}

