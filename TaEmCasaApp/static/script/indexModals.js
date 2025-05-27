function openModal(id, negocioId = null) {
  const modal = document.getElementById(id);
  modal.style.display = 'flex';

  if (negocioId != null) {
    const checkboxes = document.getElementsByName('tipo');
    const tiposSelecionados = [];

    checkboxes.forEach(chk => {
      if (chk.checked) {
        tiposSelecionados.push(chk.value);
      }
    });

    const raioElem = document.getElementsByName('raio')[0];
    const raioSelecionado = raioElem ? raioElem.value : '';

    let query = `?raio=${encodeURIComponent(raioSelecionado)}`;
    tiposSelecionados.forEach(tipo => {
      query += `&tipo=${encodeURIComponent(tipo)}`;
    });

    const form = modal.querySelector("form");
    form.action = `/login_validate/?query=${encodeURIComponent(query)}&negocio=${negocioId}`;
  }
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}

window.onclick = function(event) {
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
}
