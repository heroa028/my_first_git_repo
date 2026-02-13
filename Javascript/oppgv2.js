


function tilfeldigHilsen(username, age){
    let tilfeldigtall = Math.floor(Math.random() * 4);
    let hilsen=""
    if (tilfeldigtall == 1){
        console.log("Hei");
    }
    else if (tilfeldigtall ==2){
    console.log("Halla balla");
    }
else if (tilfeldigtall == 3){
     console.log( "Hola quicka");
}
else console.log("Du er veldig kjekk");
      
console.log( hilsen)
}


console.log(tilfeldigHilsen());

