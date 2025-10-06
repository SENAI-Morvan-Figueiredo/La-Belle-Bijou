document.querySelectorAll('.produto-card button').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation(); // impede o clique de propagar para o card
    console.log("Botão clicado sem abrir o detalhe!");
  });
});