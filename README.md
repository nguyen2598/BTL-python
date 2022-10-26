function createCouter(){
    let counter = 0
    return function increase(){
        return ++counter
    }
}
const counter1 = createCouter();
console.log(counter1())
console.log(counter1())

console.log(createCouter()())
console.log(createCouter()())
