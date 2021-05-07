$(document).ready(()=> {
  
  $(".sorter").click(() => {
    // get all products on screen
    let products = $(".product-wrapper")
    if ($(".sorter").attr("data-sort") == "title") {
      // update flag
      $(".sorter").attr("data-sort", "price")
      $(".sorter span:last").html("Price")
      // sort by price
      products.sort(sort_by_price)
      // update
      $(".products-outer-wrapper").html(products)
    }
    else if ($(".sorter").attr("data-sort") == "price") {
      // update flag
      $(".sorter").attr("data-sort", "title")
      $(".sorter span:last").html("Title")
      // sort by title
      products.sort(sort_by_title)
      // update
      $(".products-outer-wrapper").html(products)
    }
  })

  function sort_by_price(a, b) {
    let valA = parseInt($(a).find(".product-price").html().split(" ")[1])
    let valB = parseInt($(b).find(".product-price").html().split(" ")[1])
    return valA - valB
  }
  
  function sort_by_title(a, b) {
    let valA = $(a).find(".product-title").html()
    let valB = $(b).find(".product-title").html()
    if (valA < valB) {
      return -1
    }
    else if (valA > valB) {
      return 1
    }
    else {
      return 0
    }
  }
})