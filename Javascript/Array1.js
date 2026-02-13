let Primtall = [];
console.log(Primtall);


function genererPrim() {
    for (let i = 50; i > 3; i--) {
        let erPrim = true;
        for (let j = 2; j < i; j++) {
            if (i % j == 0) {
                erPrim = false;
            }
        }
        if (erPrim) {
            Primtall.push(i)
        }
    }
    
Primtall.splice(1, 46)
    console.log(Primtall);
}
genererPrim();


/*
let randomtall = [];


for (let i = 1; i < 50; i++) {
   let randomNumber = Math.round(Math.random() * 50);
    if (!randomtall.includes(randomNumber)) {
        randomtall.push(randomNumber)
    }
    console.log(randomtall);

}

  for (let numbers = 50; numbers > 0; numbers--) {
        numbers.splice(2 , 47)
        console.log(i);
    }*/