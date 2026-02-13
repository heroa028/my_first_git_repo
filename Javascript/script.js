console.log(8 + "4");
console.log(8 * "4");
console.log(8 / "4");
console.log(8 - "4");
//8+"4" gir 84 pga "" mens hvis du fjerner de så får du riktig svar//

console.log(26 - "5");
console.log(9 * "2");
console.log(28 / "2");


let a = 3;
let b = 7;
console.log(a * b);
console.log(a / b);



let antallSekunder = 9000;
let antallMinutter = (antallSekunder / 60)
let antallTimer = (antallSekunder / 3600)


console.log(antallTimer)
console.log(antallMinutter)


for (let i = 0; i <= 16; i += 2) {
    console.log(i);
}

for (let i = 16; i > 0; i -= 2) {

    //Dette gjør at du kan hoppe over tall
    if(i == 12){
        continue

    }
    else{
        console.log(i);
    }
}

for (let i = 16; i > 0; i -= 2) {

    //Dette gjør at du kan stoppe loopen på det tallet
    if(i == 12){
        break;

    }
    else{
        console.log(i);
    }
}
