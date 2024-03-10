document.querySelectorAll(".card_wrapper .remove-btn").forEach(btn=>{
    btn.addEventListener("click",()=>deleteProduct(btn));
})

function deleteProduct(btn){

    var id = btn.dataset.id;
    
    fetch(delete_url+id,{
        method:"POST",
        headers:{
            "X-CSRFToken": csrf_token
        },
    }).then(res=>{
        if(res.ok){
            btn.closet(".card_wrapper").remove();
        }
    })
    btn.closest(".card_wrapper").remove();
}