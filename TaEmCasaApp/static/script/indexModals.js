function openModal(id, negocioId = null) {
  const modal = document.getElementById(id);
  modal.style.display = 'flex';

  if (negocioId != null) {
    // Pega as checkboxes com name='tipo'
    const checkboxes = document.getElementsByName('tipo');
    const tiposSelecionados = [];

    checkboxes.forEach(chk => {
      if (chk.checked) {
        tiposSelecionados.push(chk.value);
      }
    });

    // Pega o select (ou input) com name='raio'
    const raioElem = document.getElementsByName('raio')[0];
    const raioSelecionado = raioElem ? raioElem.value : '';

    // Monta query string para tipos (array) e raio
    // Tipos vão como tipos=tipo1&tipos=tipo2, que Django entende como lista no GET
    let query = `?raio=${encodeURIComponent(raioSelecionado)}`;
    tiposSelecionados.forEach(tipo => {
      query += `&tipo=${encodeURIComponent(tipo)}`;
    });

    console.log(query)
    const form = modal.querySelector("form");
    form.action = `/taemcasa/login_validate/?query=${encodeURIComponent(query)}&negocio=${negocioId}`;
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
