// Function to update the cart count display
function updateCartCount() {
    var totalItems = 0;
    for (var i = 0; i < localStorage.length; i++) {
        if (localStorage.key(i).startsWith('product_')) {
            totalItems += parseInt(localStorage.getItem(localStorage.key(i)), 10);
        }
    }
    document.getElementById('itemCount').textContent = totalItems;
}



function updateSingleTotal(productId){
    const totalSinglePriceUzs = document.getElementById("totalSinglePriceUzs");
    const totalSinglePriceUsd = document.getElementById("totalSinglePriceUsd");
    console.log(totalSinglePriceUzs)
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const itemIndex = cart.findIndex(item => item.id === productId);
    
    if (itemIndex !== -1) {
        totalSinglePriceUzs.innerHTML = Number(cart[itemIndex].qty * cart[itemIndex].price_uzs).toLocaleString()
        totalSinglePriceUsd.innerHTML = Number(cart[itemIndex].qty * cart[itemIndex].price_usd).toLocaleString()
    }
}

// Function to save item count to localStorage
function saveItemCount(productId, count) {
    localStorage.setItem('product_' + productId, count);
}

function increaseQuantity(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const itemIndex = cart.findIndex(item => item.id === itemId);
  
    if (itemIndex !== -1) {
      cart[itemIndex].qty = 1 + Number(cart[itemIndex].qty);
      localStorage.setItem('cart', JSON.stringify(cart));
      saveItemCount(itemId, cart[itemIndex].qty);
      updateCartCount();
      updateCartDisplay();
    }

    updateSingleTotal(itemId)
}

// Function to remove an item from the cart
function removeItem(productId, productName) {
    localStorage.removeItem('product_' + productId);
    updateSingleTotal(productId)
    
    // Show Toastify notification
    Toastify({
        text: "Товар удален из корзины",
        duration: 2000,
        close: true,
        gravity: "top",
        position: "right",
        backgroundColor: "#FF0000",
        stopOnFocus: true
    }).showToast();
}
  
function decreaseQuantity(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const itemIndex = cart.findIndex(item => item.id === itemId);
    const input = document.querySelector(".amountOfProduct")
    if (input){
        input.value = cart[itemIndex].qty - 1
    }
    cart[itemIndex].qty = 1 - Number(cart[itemIndex].qty);

    if (itemIndex !== -1) {
      if (cart[itemIndex].qty === 0) {
        cart = cart.filter(item => item.id !== itemId);
        removeItem(itemId)
        if (cart.length == 0) {
            console.log(cart)
            localStorage.removeItem('cart')
        }
      }
      localStorage.setItem('cart', JSON.stringify(cart));
    }
    // saveItemCount(itemId, cart[itemIndex].qty);
    updateCartCount();
    updateCartDisplay();
    updateSingleTotal(itemId)
}

function deleteQuantity(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const itemIndex = cart.findIndex(item => item.id === itemId);
    cart.splice(itemIndex, 1);
    localStorage.setItem('cart', JSON.stringify(cart));

    removeItem(itemId);
    updateCartCount();
    updateCartDisplay();
    updateSingleTotal(itemId)
}

function updateCartDisplay() {
    const cartList = document.getElementById('cartList');
    const totalPrice = document.getElementById('totalPrice');
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let total = 0;
    
    for (let i = 0; i < cart.length; i++){
        total = total + (parseInt(cart[i].price_uzs) * parseInt(cart[i].qty));
    }

    totalPrice.innerHTML = (total).toLocaleString();
    cartList.innerHTML = cart.map(item => `<div class="row cart-modal-item">
            <div class="col-4">
                <img src="${item.cover}" class="cart-product-cover" alt="">
            </div>
            <div class="col-6">
                <div class="cart-product-title">
                    <b>${item.name}</b>
                </div>
                <div class="cart-product-code">
                    Код: #${item.id}
                </div>

                <div class="cart-product-usd">$ ${(item.price_usd).toLocaleString()}</div>
                <div class="cart-product-uzs">${Number(item.price_uzs).toLocaleString()} сум</div>
            </div>
            <div class="col-2" style="align-items: center; justify-content: center; display: flex;">
                <button onclick="deleteQuantity('${item.id}')" class="cart-delete-btn"><i class="fa fa-trash"></i></button>
            </div>
            <div class="col-2 pt-3 total-text">
                Общий:
            </div>
            <div class="col-10 pt-3">
                <div class="cart-counter-group">
                    <input type="hidden" name="productId" class="productId" value="${item.id}">
                    <input type="hidden" name="productName" class="productName" value="${item.name}">
                    <input type="hidden" name="productPriceUzs" class="productPriceUzs" value="${item.price_uzs}">
                    <input type="hidden" name="productPriceUsd" class="productPriceUsd" value="${item.price_usd}">
                    <input type="hidden" name="productCover" class="productCover" value="${item.cover}">
                    <div class="total-prices">
                        <div class="cart-total-usd">$ ${(item.price_usd * item.qty).toLocaleString()}</div>
                        <div class="cart-total-uzs">${(item.price_uzs * item.qty).toLocaleString()} сум</div>
                    </div>
                    <button onclick="decreaseQuantity('${item.id}')">-</button>
                    <input 
                        type="text" 
                        onchange="updateFromInput(event)"  
                        data-item-id="${item.id}" 
                        value="${item.qty}" 
                        style="width: 50px !important;">
                    <button 
                        onclick="increaseQuantity('${item.id}')">+</button>
                </div>
            </div>
        </div>`).join('');

    // <li>
    //         <div>
    //             <span>${item.name} (${item.qty}x${item.price_uzs} сум) ${parseInt(item.qty) * parseInt(item.price_uzs)} сум</span><br>
    //             <span>${item.name} (${item.qty}x$${item.price_usd}) $${parseInt(item.qty) * parseInt(item.price_usd)}</span>
    //         </div>
    //         <div class="cart-item-buttons">
    //             <button class="counter increase-counter" onclick="decreaseQuantity('${item.id}')">➖</button>
    //             <button class="counter decrease-counter" onclick="increaseQuantity('${item.id}')">➕</button>
    //             <button class="counter delete-counter" onclick="deleteQuantity('${item.id}')">🗑</button>
    //         </div>
    //     </li>
}


function updateFromInput(event) {
    const input = event.target;
    const itemId = input.getAttribute('data-item-id');
    const newQty = Number(input.value, 10);

    if (isNaN(newQty) || newQty < 1) {
        return
    }

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    const itemIndex = cart.findIndex(item => item.id === itemId);
    if (itemIndex !== -1) {
        cart[itemIndex].qty = newQty;
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    localStorage.setItem(`product_${itemId}`, newQty)
    updateCartCount();
    updateCartDisplay();
    input.focus();
}


document.addEventListener('DOMContentLoaded', function () {

    // Function to get item count from localStorage
    function getItemCount(productId) {
        var count = localStorage.getItem('product_' + productId);
        return count ? parseInt(count, 10) : 0;
    }



    // Function to add an item to the cart
    function addItem(productId, productName, amount, productPriceUzs, productPriceUsd, cover, fullUpdate = false) {
        var currentCount = getItemCount(productId);
        var newCount = 0;
        if (fullUpdate){
            newCount = amount;
        }else {
            newCount = currentCount + amount; // Increase the count by the input amount            
        }
        saveItemCount(productId, newCount);

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const itemIndex = cart.findIndex(item => item.id === productId);

        if (itemIndex === -1) {
            cart.push({ id: productId, name: productName, qty: newCount, price_uzs: productPriceUzs, price_usd: productPriceUsd, cover:cover });
        } else {
            cart[itemIndex].qty = newCount
        }

        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show Toastify notification
        Toastify({
            text: "Товар добавлен в корзину",
            duration: 2000,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: "#4CAF50",
            stopOnFocus: true
        }).showToast();
        
        // Update the item count display
        updateSingleTotal(productId)
        updateCartCount();
        updateCartDisplay();
    }

    // Function to clear all items from the cart
    function clearCart() {
        localStorage.clear(); // Clear total count from localStorage
        updateCartCount(); // Update count display

        Toastify({
            text: "Корзина очищена",
            duration: 2000,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: "#ff006e",
            stopOnFocus: true
        }).showToast();

        updateCartDisplay();

    }

    // Add event listeners to all "Add to Cart" buttons
    document.querySelectorAll('.add-cart').forEach(function(button) {
        button.addEventListener('click', function() {
            console.log("hello")
            var productId = this.getAttribute('data-item-id');
            var productName = this.getAttribute('data-item-name');
            var productPriceUzs = this.getAttribute('data-item-price-uzs');
            var productPriceUsd = this.getAttribute('data-item-price-usd');
            var productCover = this.getAttribute('data-item-cover');
                addItem(productId, productName, 1, productPriceUzs, productPriceUsd, productCover, fullUpdate = false);
                document.querySelector('.amountOfProduct').value = getItemCount(productId);
        });
    });

    if (document.querySelector(".amountOfProduct")){
        document.querySelector(".amountOfProduct").addEventListener("input", function() {
            let productId = document.querySelector(".productSingleId");
            let productName = document.querySelector(".productName");
            let productPriceUzs = document.querySelector(".productPriceUzs");
            let productPriceUsd = document.querySelector(".productPriceUsd");
            let productCover = document.querySelector(".productCover");
            let amount = String(document.querySelector(".amountOfProduct").value).replace(",", ".");
            
            if (productId){
                productId = productId.value;
            }
    
            if(productName){
                productName = productName.value;
            }
    
            if(productPriceUzs){
                productPriceUzs = productPriceUzs.value
            }
    
            if(productPriceUsd){
                productPriceUsd = productPriceUsd.value
            }
    
            addItem(productId, productName, amount, productPriceUzs, productPriceUsd, productCover, fullUpdate = true); 
            
        })
    }

    

    // Add event listeners to all "Remove from Cart" buttons
    document.querySelectorAll('#deleteFromCart').forEach(function(button) {
        button.addEventListener('click', function() {
            var productId = this.getAttribute('data-item-id');
            var productName = this.getAttribute('data-item-name');
            removeItem(productId, productName);
            updateCartCount();
            updateCartDisplay();
        });
    });


    document.getElementById('clearCartButton').addEventListener('click', clearCart);

    // Initialize item count display on page load
    setTimeout(()=> {
        updateCartCount();
        updateCartDisplay();
        let itemId = document.querySelector(".productId");
        console.log("Haha", itemId)
        if (itemId){
            itemId = itemId.value;
        }
        updateSingleTotal(itemId)
    }, 300)

});