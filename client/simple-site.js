// Event listener to fetch and display the results from the server.
let listfiles = document.querySelector('#Refresh');
listfiles.addEventListener('click', async function () {
    let gallery = document.getElementById('gallery');
    gallery.innerHTML ='';
    let url = 'http://localhost:8085/v1/inference'
    let res = await fetch(url);

    if (res.status == 200) {
        let json = await res.json();
        for(let i=0; i<json.length; i++){
            json[i]['file'] = await getImage(json[i]);
            previewImage(json[i]);
        }
        return;
    }

    throw new Error(res.status);
   
}, false);

// Takes a single image and text and adds them to the gallery for preview.
function previewImage(file) {
    let gallery = document.getElementById('gallery');
    let imageType = /image.*/;
 
    let thumb = document.createElement("div");
    thumb.classList.add('thumbnail'); // Add the class thumbnail to the created div
 
    let img = document.createElement("img");
    let text = document.createElement("text");
    text.appendChild(document.createTextNode((file['prediction']+" - "+file['confidence']).substring(0,15)));
    img.file = file['file'];
    thumb.appendChild(img);
    thumb.appendChild(text);
    gallery.appendChild(thumb);
 
    // Using FileReader to display the image content
    let reader = new FileReader();
    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    reader.readAsDataURL(file['file']);
}

// Since the API does not return a full image but rather a URL, we need to fetch the whole image.
async function getImage(file) {
    let url = 'http://localhost:8085'+file['img_url']
    let res = await fetch(url);
    if (res.status == 200) {
        let file = await res.blob();
        return file;
    }
    return null;

}

// POST request to the server.
async function uploadFile(file){
    let url = 'http://localhost:8085/v1/inference';
    let fd = new FormData();
    fd.append("file_name", file);
    let res = await fetch(url, {method: 'POST', body: fd})
    console.log( await res.json());
    document.querySelector('#Refresh').click();
}

// Handle the file uploads.
let uploadfiles = document.querySelector('#uploadfiles');
uploadfiles.addEventListener('change', function () {
    let files = this.files;
    for(let i=0; i<files.length; i++){
        uploadFile(this.files[i]);
    }
}, false);
