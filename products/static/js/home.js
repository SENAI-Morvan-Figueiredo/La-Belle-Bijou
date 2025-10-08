document.addEventListener("DOMContentLoaded", function() {
  const track = document.querySelector('.carousel-track');
  const items = Array.from(document.querySelectorAll('.produto-card'));
  const prevBtn = document.querySelector('.carousel-btn.prev');
  const nextBtn = document.querySelector('.carousel-btn.next');
  
  let currentIndex = 0;
  let itemsPerView = 4; // padrão desktop
  const moveBy = 2; // desliza 2 por clique

  function updateItemsPerView() {
    const width = window.innerWidth;
    if (width <= 700) itemsPerView = 2;
    else if (width <= 1000) itemsPerView = 3;
    else itemsPerView = 4;
  }

  function updateCarousel() {
    const itemWidth = items[0].offsetWidth + 80; // soma o gap (aprox. 2rem)
    const moveX = currentIndex * itemWidth;
    track.style.transform = `translateX(-${moveX}px)`;
  }

  nextBtn.addEventListener('click', () => {
    updateItemsPerView();
    if (currentIndex + moveBy < items.length - itemsPerView + 1) {
      currentIndex += moveBy;
      updateCarousel();
    }
  });

  prevBtn.addEventListener('click', () => {
    updateItemsPerView();
    if (currentIndex - moveBy >= 0) {
      currentIndex -= moveBy;
      updateCarousel();
    }
  });

  window.addEventListener('resize', () => {
    updateItemsPerView();
    updateCarousel();
  });

  updateItemsPerView();
});