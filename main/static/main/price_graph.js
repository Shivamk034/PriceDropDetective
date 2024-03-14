

function convertPrice(price_str) {  
    return parseFloat(price_str.replace(/[^0-9.]/g, ''))
}
// prices_obj = [ {price:XXXX, time:XXXX },...]
prices_obj = prices_obj.map((obj) => {
    var price = convertPrice(obj.price);
    var time = new Date(obj.time);
    return {
        ...obj,
        price,
        time,
    }
})


console.log(prices_obj);
console.log(prices_obj[0].time);


const data = prices_obj.map((obj)=>{
    return obj.price;
    // return {
    //     x:Date.parse(obj.time),
    //     y:obj.price,
    // }
})

const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

var labels = prices_obj.map((obj)=>{
    return obj.time.toDateString();
});

var last_date = new Date(Date.parse(prices_obj[prices_obj.length-1].time));
// console.log("last_date:",last_date);
for (var i=0;i<2;i++){
    last_date = new Date(last_date.setDate(last_date.getDate()+1));
    
    // console.log(last_date);
    labels.push(last_date.toDateString());
}

const main_data = {
    labels: labels,
    datasets: [{
        label: 'Price',
        data: data,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
    }]
};

const chart = new Chart(ctx, {
    type: 'line',
    data: main_data,
});

document.querySelector(".graph-section .graph").append(canvas);