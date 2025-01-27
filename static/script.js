var currently_selected = null;

async function expand_item(id) {
  if (currently_selected != null) {
    document.getElementById(currently_selected).nextSibling.remove();
    if (currently_selected == id) {
      currently_selected = null;
      return;
    }
  }

  let html = "";
  try {
    let response = await fetch(
      `inventory/item/${document.getElementById(id).cells[1].innerHTML}`,
    );

    html = await response.text();
    // console.log(html);
  } catch (e) {}

  let el = document.createElement("tr");
  el.innerHTML = `<td colspan="7">${html}</td>`;

  document.getElementById(id).insertAdjacentElement("afterend", el);
  currently_selected = id;
}
