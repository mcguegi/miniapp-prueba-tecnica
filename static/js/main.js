window.onload = function(){
    let cantidadCampo =document.getElementById("cantidad");
    cantidadCampo.onkeypress = function (evt){
        evt.preventDefault();
    };
}

function actualizarPrecio(valor) {
    let precioProducto = document.getElementById("product_price1").getAttribute('value');
    var precio = document.getElementById("totalC");
    precio.value = "$" + valor* precioProducto;
}
