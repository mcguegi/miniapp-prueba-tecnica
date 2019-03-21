window.onload = function(){
    let cantidadCampo =document.getElementById("cantidad");
    cantidadCampo.onkeypress = function (evt){
        evt.preventDefault();
    };
}

function actualizarPrecio(valor) {
    let precioProducto = 100;
    var precio = document.getElementById("totalC");
    precio.value = "$" + valor*precioProducto;
}
