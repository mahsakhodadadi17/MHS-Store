const orders = [
  {id:"#1001", name:"Ali", status:"paid", price:120},
  {id:"#1002", name:"Sara", status:"shipping", price:340},
  {id:"#1003", name:"John", status:"cancel", price:90},
  {id:"#1004", name:"Mina", status:"paid", price:220},
];

const tbody = document.getElementById("tbody");
const search = document.getElementById("search");
const filter = document.getElementById("filter");

function render(data){
  tbody.innerHTML = "";

  data.forEach(o=>{
    tbody.innerHTML += `
      <tr>
        <td>${o.id}</td>
        <td>${o.name}</td>
        <td><span class="badge ${o.status}">${o.status}</span></td>
        <td>$${o.price}</td>
        <td>
          <button class="btn view" onclick="openModal('${o.id}')">View</button>
          <button class="btn del" onclick="removeOrder('${o.id}')">Delete</button>
        </td>
      </tr>
    `;
  });
}

function applyFilters(){
  const q = search.value.toLowerCase();
  const f = filter.value;

  const result = orders.filter(o=>{
    const matchSearch = o.name.toLowerCase().includes(q) || o.id.includes(q);
    const matchFilter = f === "all" || o.status === f;
    return matchSearch && matchFilter;
  });

  render(result);
}

search.addEventListener("input", applyFilters);
filter.addEventListener("change", applyFilters);

function removeOrder(id){
  const i = orders.findIndex(o=>o.id===id);
  orders.splice(i,1);
  showToast("Order deleted");
  applyFilters();
}

function openModal(id){
  const o = orders.find(x=>x.id===id);

  document.getElementById("modalContent").innerHTML = `
    <p><b>ID:</b> ${o.id}</p>
    <p><b>Name:</b> ${o.name}</p>
    <p><b>Status:</b> ${o.status}</p>
    <p><b>Price:</b> $${o.price}</p>
  `;

  document.getElementById("modal").style.display="flex";
}

function closeModal(){
  document.getElementById("modal").style.display="none";
}

function toggleTheme(){
  document.body.classList.toggle("dark");
}

function showToast(msg){
  const t = document.getElementById("toast");
  t.innerText = msg;
  t.style.display = "block";

  setTimeout(()=>{
    t.style.display = "none";
  },2000);
}

render(orders);