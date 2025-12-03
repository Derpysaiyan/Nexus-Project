function wireLogoutButtons() {
  const logoutButtons = document.querySelectorAll('.js-logout');
  logoutButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      clearUser();   // remove stored user
      cart = [];     // clear cart
      saveCart();

      window.location.href = 'login.html';
    });
  });
}



let cart = [];

function loadUser() {
  try {
    const raw = localStorage.getItem("nexusUser");
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

function saveUser(user) {
  try {
    localStorage.setItem("nexusUser", JSON.stringify(user));
  } catch (e) {}
}

function clearUser() {
  localStorage.removeItem("nexusUser");
}

function loadCart() {
  try {
    const raw = localStorage.getItem("nexusCart");
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveCart() {
  try {
    localStorage.setItem("nexusCart", JSON.stringify(cart));
  } catch (e) {
    
  }
}

function updateCartCount() {
  const countEls = document.querySelectorAll(".js-cart-count");
  if (!countEls.length) return;

  const totalQty = cart.reduce((sum, item) => sum + (item.qty || 0), 0);
  countEls.forEach((el) => {
    el.textContent = totalQty;
  });
}

function addToCart(product, qty) {
  if (!qty || qty <= 0) return;

  const existing = cart.find((item) => item.id === product.id);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({ ...product, qty });
  }
  saveCart();
  updateCartCount();
}



function loadOrders() {
  try {
    const raw = localStorage.getItem("nexusOrders");
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveOrders(orders) {
  try {
    localStorage.setItem("nexusOrders", JSON.stringify(orders));
  } catch (e) {
    
  }
}



document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;

  
  cart = loadCart();
  updateCartCount();

  
  wireLogoutButtons();

  if (page === "login") {
    initLogin();
  } else if (page === "signup") {
    initSignup();
  } else if (page === "catalog") {
    initCatalog();
  } else if (page === "cart") {
    initCartPage();
  } else if (page === "checkout") {
    initCheckoutPage();
  } else if (page === "orders") {
    initOrdersPage && initOrdersPage();
  }
});




function initLogin() {
  const form = document.getElementById("loginForm");
  if (!form) return;

  const errorMsg = document.getElementById("loginErr");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    fetch("http://127.0.0.1:5000/Login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ Email: email, Password: password })
    })
      .then(res => res.json().then(data => ({ status: res.status, data })))
      .then(result => {
        if (result.status !== 200) {
          errorMsg.textContent = result.data.error || "Invalid login.";
          errorMsg.style.display = "block";
          return;
        }

        // Save login
        saveUser({
          User_ID: result.data.User_ID,
          Name: result.data.Name,
          Role: result.data.Role
        });

        errorMsg.style.display = "none";
        window.location.href = "catalog.html";
      })
      .catch(() => {
        errorMsg.textContent = "Server error. Try again later.";
        errorMsg.style.display = "block";
      });
  });
}

function initSignup() {
  const form = document.getElementById("signupForm");
  if (!form) return;

  const errorMsg = document.getElementById("signupErr");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    fetch("http://127.0.0.1:5000/Signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ Name: name, Email: email, Password: password })
    })
      .then(res => res.json().then(data => ({ status: res.status, data })))
      .then(result => {
        if (result.status !== 200) {
          errorMsg.textContent = result.data.error || "Unable to sign up.";
          errorMsg.style.display = "block";
          return;
        }

        // Save user immediately after signup
        saveUser({
          User_ID: result.data.User_ID,
          Name: result.data.Name,
          Role: result.data.Role
        });

        window.location.href = "catalog.html";
      })
      .catch(() => {
        errorMsg.textContent = "Server error. Try again.";
        errorMsg.style.display = "block";
      });
  });
}




function initCatalog() {
  let products = [];

  const grid = document.getElementById("productGrid");
  const brandFilter = document.getElementById("brandFilter");
  const priceFilter = document.getElementById("priceFilter");
  const searchInput =
    document.getElementById("topSearch") ||
    document.getElementById("searchInput");

  if (!grid) return;

  
  function renderProducts(list) {
    grid.innerHTML = "";

    if (!list.length) {
      grid.innerHTML =
        '<p class="catalog-empty">No phones match your filters.</p>';
      return;
    }

    list.forEach((p) => {
      const card = document.createElement("article");
      card.className = "product-card";

      card.innerHTML = `
        <div class="product-image-wrap">
          <img src="${p.image}" alt="${p.name}" />
        </div>

        <h3 class="product-name">${p.name}</h3>
        <p class="product-brand">${p.brand}</p>

        <div class="product-rating">
          <span class="product-stars">★★★★☆</span>
          <span class="product-reviews">${p.reviews}</span>
        </div>

        <div class="product-price">$${p.price.toFixed(2)}</div>

        <div class="product-actions">
          <select class="product-qty">
            <option value="1">Qty: 1</option>
            <option value="2">Qty: 2</option>
            <option value="3">Qty: 3</option>
            <option value="4">Qty: 4</option>
            <option value="5">Qty: 5</option>
          </select>
          <button class="btn product-btn" type="button">Add to Cart</button>
        </div>
      `;

      const qtySelect = card.querySelector(".product-qty");
      const addBtn = card.querySelector(".product-btn");

      addBtn.addEventListener("click", () => {
        const qty = parseInt(qtySelect.value, 10) || 1;
        addToCart(p, qty);
      });

      grid.appendChild(card);
    });
  }

  
  function applyFilters() {
    let list = [...products];

    const brandValue = brandFilter?.value || "all";
    const priceValue = priceFilter?.value || "all";
    const searchValue = (searchInput?.value || "").toLowerCase().trim();

    if (brandValue !== "all") {
      list = list.filter((p) => p.brand.trim().toLowerCase() === brandValue.trim().toLowerCase());
    }
    
    if (priceValue !== "all") {
      list = list.filter((p) => {
        if (priceValue === "under-800") return p.price < 800;
        if (priceValue === "800-1000") return p.price >= 800 && p.price <= 1000;
        if (priceValue === "over-1000") return p.price > 1000;
        return true;
      });
    }

    
    if (searchValue) {
      list = list.filter((p) =>
        p.name.toLowerCase().includes(searchValue)
      );
    }

    renderProducts(list);
  }

  brandFilter?.addEventListener("change", applyFilters);
  priceFilter?.addEventListener("change", applyFilters);
  searchInput?.addEventListener("input", applyFilters);

  
  fetch("http://127.0.0.1:5000/Products")
    .then(res => res.json())
    .then(data => {
      // convert backend fields to frontend fields
      products = data.map(p => ({
        id: p.Product_ID,
        name: p.Name,
        brand: p.BrandName,
        price: p.Price,
        image: p.Image,
        reviews: p.Review_Count
      }));

      applyFilters();
    })
    .catch(err => {
      console.error("Failed to load products:", err);
    });
}





function initCartPage() {
  const content = document.getElementById("cartContent");
  if (!content) return;

  cart = loadCart();
  updateCartCount();

  function renderCart() {
    content.innerHTML = "";

    if (!cart.length) {
      content.innerHTML =
        '<p class="cart-empty">Your cart is empty. Go back to the catalog and add some phones.</p>';
      return;
    }

    let subtotal = 0;

    const list = document.createElement("div");
    list.className = "cart-list";

    cart.forEach((item) => {
      const row = document.createElement("div");
      row.className = "cart-row";

      const lineTotal = item.price * item.qty;
      subtotal += lineTotal;

      const imgSrc = item.image || "Iphone15_128gb.jpg";

      row.innerHTML = `
        <div class="cart-row-left">
          <div class="cart-row-image">
            <img src="${imgSrc}" alt="${item.name}">
          </div>
          <div class="cart-row-info">
            <div class="cart-row-name">${item.name}</div>
            <div class="cart-row-brand">${item.brand}</div>
          </div>
        </div>

        <div class="cart-row-right">
          <div class="cart-row-qty">Qty: ${item.qty}</div>
          <div class="cart-row-price">$${lineTotal.toFixed(2)}</div>
          <button
            class="cart-remove-btn"
            type="button"
            data-id="${item.id}"
          >
            Remove
          </button>
        </div>
      `;

      list.appendChild(row);
    });

    const summary = document.createElement("div");
    summary.className = "cart-summary";
    summary.innerHTML = `
      <div class="cart-summary-line">
        Subtotal (${cart.length} items):
        <span>$${subtotal.toFixed(2)}</span>
      </div>
      <button class="btn cart-checkout-btn" type="button">
        Proceed to checkout
      </button>
    `;

    content.appendChild(list);
    content.appendChild(summary);

    
    list.addEventListener("click", (e) => {
      if (e.target.classList.contains("cart-remove-btn")) {
        const id = Number(e.target.dataset.id);
        cart = cart.filter((item) => item.id !== id);
        saveCart();
        updateCartCount();
        renderCart();
      }
    });

    
    const checkoutBtn = summary.querySelector(".cart-checkout-btn");
    checkoutBtn.addEventListener("click", () => {
      window.location.href = "checkout.html";
    });
  }

  renderCart();
}



function initCheckoutPage() {
  const itemsContainer = document.getElementById("checkoutItems");
  const summaryContainer = document.getElementById("checkoutSummary");
  const countEl = document.getElementById("checkoutItemsCount");

  if (!itemsContainer || !summaryContainer) return;

  cart = loadCart();
  updateCartCount();

  if (!cart.length) {
    itemsContainer.innerHTML =
      '<p class="checkout-empty">Your cart is empty. Go back to the catalog and add some phones.</p>';
    summaryContainer.innerHTML = "";
    if (countEl) countEl.textContent = "";
    return;
  }

  let subtotal = 0;
  let totalQty = 0;

  
  const shippingByItem = {};

  itemsContainer.innerHTML = "";

  cart.forEach((item) => {
    const lineTotal = item.price * item.qty;
    subtotal += lineTotal;
    totalQty += item.qty;

    const imgSrc = item.image || "Iphone15_128gb.jpg";

    const row = document.createElement("article");
    row.className = "checkout-item";

    row.innerHTML = `
      <div class="checkout-item-top">
        <div class="checkout-item-left">
          <div class="checkout-item-image">
            <img src="${imgSrc}" alt="${item.name}">
          </div>
          <div class="checkout-item-info">
            <div class="checkout-item-name">${item.name}</div>
            <div class="checkout-item-meta">
              Qty: ${item.qty} &bull;
              $${item.price.toFixed(2)} each
            </div>
            <div class="checkout-item-line-total">
              Item total: $${lineTotal.toFixed(2)}
            </div>
          </div>
        </div>

        <div class="checkout-item-delivery">
          <div class="delivery-label">Choose a delivery option:</div>
          <label class="delivery-option">
            <input type="radio" name="shipping-${item.id}" checked>
            Free delivery (3–5 business days)
          </label>
          <label class="delivery-option">
            <input type="radio" name="shipping-${item.id}">
            $4.99 — Faster delivery (2–3 business days)
          </label>
          <label class="delivery-option">
            <input type="radio" name="shipping-${item.id}">
            $9.99 — Priority (next business day)
          </label>
        </div>
      </div>
    `;

    itemsContainer.appendChild(row);

    
    const radios = row.querySelectorAll(`input[name="shipping-${item.id}"]`);
    radios.forEach((radio, index) => {
      let shipCost = 0;
      if (index === 1) shipCost = 4.99;
      if (index === 2) shipCost = 9.99;

      if (index === 0) {
        
        shippingByItem[item.id] = shipCost;
      }

      radio.addEventListener("change", () => {
        if (radio.checked) {
          shippingByItem[item.id] = shipCost;
          updateSummaryValues();
        }
      });
    });
  });

  if (countEl) {
    countEl.textContent = `(${totalQty} item${totalQty !== 1 ? "s" : ""})`;
  }

  const taxRate = 0.10; 

  function computeShipping() {
    return Object.values(shippingByItem).reduce((sum, v) => sum + v, 0);
  }

  
  summaryContainer.innerHTML = `
    <div class="checkout-summary-card">
      <h2>Order Summary</h2>

      <div class="checkout-summary-line">
        <span>Items (${totalQty}):</span>
        <span>$${subtotal.toFixed(2)}</span>
      </div>
      <div class="checkout-summary-line">
        <span>Shipping &amp; handling:</span>
        <span class="js-ship">$0.00</span>
      </div>
      <div class="checkout-summary-line">
        <span>Total before tax:</span>
        <span class="js-before-tax">$0.00</span>
      </div>
      <div class="checkout-summary-line">
        <span>Estimated tax (10%):</span>
        <span class="js-tax">$0.00</span>
      </div>

      <div class="checkout-summary-total">
        <span>Order total:</span>
        <span class="checkout-summary-total-amount js-total">
          $0.00
        </span>
      </div>

      <button class="btn checkout-place-order-btn" type="button">
        Place your order
      </button>
    </div>
  `;

  const shipSpan = summaryContainer.querySelector(".js-ship");
  const beforeTaxSpan = summaryContainer.querySelector(".js-before-tax");
  const taxSpan = summaryContainer.querySelector(".js-tax");
  const totalSpan = summaryContainer.querySelector(".js-total");
  const placeOrderBtn = summaryContainer.querySelector(
    ".checkout-place-order-btn"
  );

  function updateSummaryValues() {
    const shipping = computeShipping();
    const beforeTax = subtotal + shipping;
    const tax = beforeTax * taxRate;
    const total = beforeTax + tax;

    shipSpan.textContent = `$${shipping.toFixed(2)}`;
    beforeTaxSpan.textContent = `$${beforeTax.toFixed(2)}`;
    taxSpan.textContent = `$${tax.toFixed(2)}`;
    totalSpan.textContent = `$${total.toFixed(2)}`;
  }

  
  updateSummaryValues();

  
placeOrderBtn.addEventListener("click", () => {
  const user = loadUser();
  if (!user) {
    alert("You must be logged in to place an order.");
    window.location.href = "login.html";
    return;
  }

  // Builds the  backend order object
  const orderPayload = {
    User_ID: user.User_ID,
    Total: Number(totalSpan.textContent.replace("$", "")),
    Items: cart.map(item => ({
      Product_ID: item.id,
      Quantity: item.qty,
      Price: item.price
    }))
  };

  fetch("http://127.0.0.1:5000/Orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orderPayload)
  })
    .then(res => res.json().then(data => ({ status: res.status, data })))
    .then(result => {
      if (result.status !== 201) {
        alert(result.data.error || "Could not place your order.");
        return;
      }

      // Order succeeded!
      cart = [];
      saveCart();
      updateCartCount();

      window.location.href = "orders.html";
    })
    .catch(() => {
      alert("Server error. Try again later.");
    });
});


}



function initOrdersPage() {
  const container = document.getElementById("ordersContent");
  if (!container) return;

  const user = loadUser();
  if (!user) {
    container.innerHTML = "<p>You must log in to see your orders.</p>";
    return;
  }

  cart = loadCart();
  updateCartCount();

  fetch(`http://127.0.0.1:5000/Orders/user/${user.User_ID}`)
    .then(res => res.json())
    .then(orders => {
      if (!orders.length) {
        container.innerHTML =
          '<p class="orders-empty">You have no orders yet. Place an order from the catalog.</p>';
        return;
      }

      container.innerHTML = "";

      // Latest first
      orders.slice().reverse().forEach(order => {
        const orderId = order.Order_ID;
        const orderDate = order.Order_date?.split(" ")[0] || "Unknown date";

        let itemsHtml = "";
        order.Items.forEach(item => {
          const imgSrc = item.Image || "Images/Iphone15_128gb.jpg";
          itemsHtml += `
            <div class="order-item-row">
              <div class="order-item-image">
                <img src="${imgSrc}" alt="${item.Name}">
              </div>
              <div class="order-item-info">
                <div class="order-item-name">${item.Name}</div>
                <div class="order-item-meta">
                  Qty: ${item.Quantity} &bull; $${item.Price.toFixed(2)} each
                </div>
              </div>
            </div>
          `;
        });

        const total = order.Total_price || 0;

        const card = document.createElement("article");
        card.className = "order-card";
        card.innerHTML = `
          <div class="order-card-header">
            <div class="order-card-meta">
              <div>
                <span class="order-card-label">Order placed:</span>
                <span>${orderDate}</span>
              </div>
              <div>
                <span class="order-card-label">Order ID:</span>
                <span>${orderId}</span>
              </div>
            </div>
            <div class="order-card-total">
              <div class="order-card-label">Order total:</div>
              <div class="order-card-total-amount">$${total.toFixed(2)}</div>
            </div>
          </div>

          <div class="order-card-body">
            <div class="order-items-list">${itemsHtml}</div>
          </div>
        `;

        container.appendChild(card);
      });
    })
    .catch(() => {
      container.innerHTML = "<p>Failed to load your orders.</p>";
    });
}





