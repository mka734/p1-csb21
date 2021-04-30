let alertElems = document.getElementsByClassName('alert-box');
let closeElems = document.getElementsByClassName('close');

window.setTimeout(() => {
  for (let i = 0; i < alertElems.length; i++) {
    alertElems[i].remove();
  }
}, 8000);

for (let i = 0; i < closeElems.length; i++) {
  closeElems[i].addEventListener('click', () => {
    closeElems[i].parentNode.remove();
  });
}
