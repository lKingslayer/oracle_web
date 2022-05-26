function openChant(img){
    var source = img.src;
    var src = document.getElementById("img").src;
    window.open('/static/handa/H/characters/H10152-1-1039.png');
    //window.open(source);
    source = source.replace('/static/','');
    source = './' + source;

    const fs = require('fs');

    let rawdata = fs.readFileSync('/static/db_to_handa.json','utf8');
    let handa = JSON.parse(rawdata);
    //console.log(handa);
    //window.open("/static/handa/"+ handa["./ocr_char/0394/甲骨文字編-李宗焜_0277_11_0_0394_次_17935(AB).png"][0]);
    //window.open('/static/handa/H/characters/H10152-1-1039.png');

    for(var key in handa){
    if (obj.hasOwnProperty(key)){
        if (source == key){
            var value=handa[key];
            let first = '/static/handa/'+value[0];
            console.log(first);
            window.open(first);
            }
        }
    }
    console.log(handa);

}
