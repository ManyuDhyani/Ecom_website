$('#slider1, #slider2, #slider3').owlCarousel({
 loop:true,
 margin:20,
 responsiveClass:true,
 responsive:{
     0:{
         items:1,
         nav:false,
         autoplay: true,
     },
     600:{
         items:3,
         nav:true,
         autoplay: true,
     },
     1000:{
         items:5,
         nav:true,
         loop:true,
         autoplay: true,
     }
 }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var qty = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){
            qty.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var qty = this.parentNode.children[2]
    var removed_item = this
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            qty.innerText = data.quantity
            if (Number(data.quantity) == 0) {
                console.log("remove")
                removed_item.parentNode.parentNode.parentNode.parentNode.remove()
            }
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.total_amount

        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var removed_item = this
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.total_amount
            removed_item.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})