/* A função escolhaCampo permite que apenas um dos campos sejam preenchidos */
function escolhaCampo(outroCampoId, campoAtual) {
    const outroCampo = document.getElementById(outroCampoId);
    if (campoAtual.value.trim() !== "") {
        outroCampo.value = ""; 
    }
}
