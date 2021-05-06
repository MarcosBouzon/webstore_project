$(document).ready(() => {
  showCartWindow()
  addCartItem()
})

// open modal on click over cart icon
function showCartWindow() {
  // get cart trigger
  let cart = $(".cart-badge-wrapper")
  // initialize modal
  let cartModal = new bootstrap.Modal(document.getElementById('cart-modal'))
  // show on click
  cart.click(() => {
    // get cart items from server
    getCartItems()
    // show modal
    cartModal.toggle()
  })
}

// get current cart items from server
function getCartItems() {
  let url = "/cart/"
  // init ajax request
  $.getJSON(url, (data, status, xhr) => {
    renderCartItems(data)
  })
}

// render cart items in modal window
function renderCartItems(items) {
  // get modal body
  let body = $("#cart-modal tbody")
  // clean body
  body.empty()
  // insert elements into cart modal
  $.each(items, function(id, item){
    body.append(`
      <tr>
        <td class="d-none">${item.id}</td>
        <td>${item.product.id}</td>
        <td>${item.product.name}</td>
        <td>$ ${item.product.price.toLocaleString("EN-en")}</td>
        <td><span class="material-icons">delete_forever</span></td>
      </tr>
    `)
  });
  $("#cart-modal .modal-header h5").html(`Cart Items: ${items.length}`)
  // enable deletion of items from cart
  delCartItem()
}

// add items to cart
function addCartItem() {
  // get trigger
  let add_trigger = $(".buttons-wrapper a.add-item")
  // on click
  add_trigger.click(function(e) {
    // prevent default behaviors
    e.preventDefault()
    e.stopPropagation()
    // get item from url
    let item_id = document.location.pathname.split("/")
    item_id = item_id[item_id.length - 2]
    // ajax request
    $.ajax("/cart/", {
      method: "post",
      data: {action: "add", id: item_id},
      headers: {"X-CSRFToken": csrftoken},
      success: (status, data, xhr) => {
        // get cart badge counter
        let badge_counter = $(".cart-content-counter")
        // increase counter
        if (badge_counter.html().length) {
          badge_counter = badge_counter.html(parseInt(badge_counter.html()) + 1)
        }
        // cart is empty
        else {
          badge_counter = badge_counter.html(1)
        }
        // show status message
        $(".messages-wrapper").remove()
        $("body").append(
          `
          <div class="messages-wrapper col-12">
            <div class="row mx-0 justify-content-center">
              <div class="alert alert-dismissible fade show alert-success col-12 col-md-10 col-lg-8" role="alert">
                Your product have been added to the cart!.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>
          </div>`
        )
      },
      error: () => {
        $(".messages-wrapper").remove()
        $("body").append(
          `
          <div class="messages-wrapper col-12">
            <div class="row mx-0 justify-content-center">
              <div class="alert alert-dismissible fade show alert-error col-12 col-md-10 col-lg-8" role="alert">
                Sorry, your product cannot be added at this time, try again later.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>
          </div>`
        )
      }
      
    })
  })
}

// remove items from cart
function delCartItem() {
  // get trigger
  let del_trigger = $(".modal .modal-body td span")
  // on click
  del_trigger.click(function() {
    // get item from url
    let tr = $(this).parent().parent()
    item_id = tr.find("td")[0]
    item_id = $(item_id).html()
    // ajax request
    $.ajax("/cart/", {
      method: "post",
      data: {action: "del", id: item_id},
      headers: {"X-CSRFToken": csrftoken},
      success: (status, data, xhr) => {
        // get cart badge counter
        let badge_counter = $(".cart-content-counter")
        // increase counter
        if (parseInt(badge_counter.html()) > 1) {
          badge_counter = badge_counter.html(parseInt(badge_counter.html()) - 1)
        }
        // cart is empty
        else {
          badge_counter = badge_counter.html("")
        }
        // remove element from the dom
        $(tr).remove()
        // show status message
        $(".messages-wrapper").remove()
        $("body").append(
          `
          <div class="messages-wrapper col-12">
            <div class="row mx-0 justify-content-center">
              <div class="alert alert-dismissible fade show alert-success col-12 col-md-10 col-lg-8" role="alert">
                Product has been removed from the cart.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>
          </div>`
        )
      },
      error: () => {
        $(".messages-wrapper").remove()
        $("body").append(
          `
          <div class="messages-wrapper col-12">
            <div class="row mx-0 justify-content-center">
              <div class="alert alert-dismissible fade show alert-error col-12 col-md-10 col-lg-8" role="alert">
                Sorry, your product cannot be removed at this time, try again later.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>
          </div>`
        )
      }
      
    })
  })
}










