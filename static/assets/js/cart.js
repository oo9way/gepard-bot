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
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const itemIndex = cart.findIndex(item => item.id === productId);
    
    if (itemIndex !== -1) {
        totalSinglePriceUzs.innerHTML = Number(cart[itemIndex].qty * cart[itemIndex].price).toLocaleString()
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
      cart[itemIndex].qty += 1;
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
        text: "Mahsulot savatdan olib tashlandi",
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
    cart[itemIndex].qty -= 1;

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
        total = total + (parseInt(cart[i].price) * parseInt(cart[i].qty));
    }

    totalPrice.innerHTML = total;
    cartList.innerHTML = cart.map(item => `
        <li>
            <div>
                <span>${item.name} (${item.qty}x${item.price} so'm) ${parseInt(item.qty) * parseInt(item.price)} so'm</span>
            </div>
            <div class="cart-item-buttons">
                <button class="counter increase-counter" onclick="decreaseQuantity('${item.id}')">➖</button>
                <button class="counter decrease-counter" onclick="increaseQuantity('${item.id}')">➕</button>
                <button class="counter delete-counter" onclick="deleteQuantity('${item.id}')">🗑</button>
            </div>
        </li>
    `).join('');
}


document.addEventListener('DOMContentLoaded', function () {

    // Function to get item count from localStorage
    function getItemCount(productId) {
        var count = localStorage.getItem('product_' + productId);
        return count ? parseInt(count, 10) : 0;
    }



    // Function to add an item to the cart
    function addItem(productId, productName, amount, productPrice) {
        var currentCount = getItemCount(productId);
        var newCount = currentCount + amount; // Increase the count by the input amount
        saveItemCount(productId, newCount);

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const itemIndex = cart.findIndex(item => item.id === productId);

        if (itemIndex === -1) {
            cart.push({ id: productId, name: productName, qty: newCount, price: productPrice });
        } else {
            cart[itemIndex].qty = newCount
        }

        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show Toastify notification
        Toastify({
            text: amount + "ta mahsulot savatga qo'shildi",
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
            text: "Savatcha tozalandi",
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
            var productId = this.getAttribute('data-item-id');
            var productName = this.getAttribute('data-item-name');
            var productPrice = this.getAttribute('data-item-price');
                addItem(productId, productName, 1, productPrice);
                document.querySelector('.amountOfProduct').value = getItemCount(productId);
        });
    });

    

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
    }, 300)

});