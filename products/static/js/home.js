document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector('.carousel-track .produtos-grid');
  const prevBtn = document.querySelector('.carousel-btn.prev');
  const nextBtn = document.querySelector('.carousel-btn.next');

  const cardWidth = document.querySelector('.produto-card').offsetWidth + 80; // largura + gap
  let position = 0;

  // Ao clicar em "next", o carrossel vai para a esquerda (mostra novos itens à direita)
  nextBtn.addEventListener('click', () => {
    const maxScroll = -(track.scrollWidth - track.parentElement.offsetWidth);
    position -= cardWidth * 2; // move 2 produtos por vez
    if (position < maxScroll) position = maxScroll;
    track.style.transform = `translateX(${position}px)`;
  });

  // Ao clicar em "prev", o carrossel vai para a direita (volta para itens anteriores)
  prevBtn.addEventListener('click', () => {
    position += cardWidth * 2;
    if (position > 0) position = 0;
    track.style.transform = `translateX(${position}px)`;
  });
});