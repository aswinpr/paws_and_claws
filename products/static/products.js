(function() {
  'use strict';

  // Mark script as loaded
  window.productsFilterLoaded = true;

  document.addEventListener("DOMContentLoaded", function() {
    
    var filterButtons = document.querySelectorAll(".filter");
    var productCards = document.querySelectorAll(".product-card");
    var countEl = document.getElementById("count");

    if (filterButtons.length === 0 || productCards.length === 0) {
      return;
    }

    function updateCount(visible, total) {
      if (!countEl) return;
      countEl.textContent = "Showing " + visible + " of " + total;
    }

    // Function to filter products
    function filterProducts(category) {
      var i;
      var card;
      var cardCategory;
      var cardCatLower;
      var selectedCatLower;
      var total = productCards.length;
      var visible = 0;
      
      for (i = 0; i < productCards.length; i++) {
        card = productCards[i];
        cardCategory = card.getAttribute("data-category");
        
        // If "all" is selected, show everything
        if (category === "all" || !category) {
          card.style.display = "flex";
          visible++;
        } else {
          // Compare categories (case-insensitive)
          cardCatLower = cardCategory ? cardCategory.toLowerCase().trim() : "";
          selectedCatLower = category ? category.toLowerCase().trim() : "";
          
          if (cardCatLower === selectedCatLower) {
            card.style.display = "flex";
            visible++;
          } else {
            card.style.display = "none";
          }
        }
      }

      updateCount(visible, total);
    }

    // Add click event listeners to filter buttons
    var i;
    for (i = 0; i < filterButtons.length; i++) {
      filterButtons[i].addEventListener("click", function() {
        var j;
        var category;
        
        // Remove active class from all buttons
        for (j = 0; j < filterButtons.length; j++) {
          filterButtons[j].classList.remove("active");
        }
        
        // Add active class to clicked button
        this.classList.add("active");
        
        // Get the category from data attribute
        category = this.getAttribute("data-category");
        
        // Filter products
        filterProducts(category);
      });
    }

    // Ensure all products are visible on page load
    filterProducts("all");
  });

})();
