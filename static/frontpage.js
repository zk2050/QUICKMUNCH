function AddStore() {
    let item = document.getElementById("store-place-holder");
    var new_Item = item.cloneNode(true);
    let grid = document.getElementById("container");
    grid.appendChild(new_Item);
    
}