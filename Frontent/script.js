const data = [
  { name: "Irfan", reg: "MGP24CS001", lab: "RB Systems lab", issue: "09:30 AM", return: "-", status: "Issued" },
  { name: "Priya S", reg: "MGPCS24015", lab: "RB algorithm Lab", issue: "10:15 AM", return: "-", status: "Issued" },
  { name: "Arya Mohan", reg: "MGPCS24008", lab: "RB Research Lab", issue: "08:00 AM", return: "11:30 AM", status: "Returned" }
];

const tbody = document.getElementById("tableBody");
const searchInput = document.getElementById("searchInput");

function renderTable(filter = "") {
  tbody.innerHTML = "";
  let issued = 0;
  let returned = 0;

  data.forEach(row => {
    if (
      row.name.toLowerCase().includes(filter) ||
      row.reg.toLowerCase().includes(filter) ||
      row.lab.toLowerCase().includes(filter)
    ) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.name}</td>
        <td>${row.reg}</td>
        <td>${row.lab}</td>
        <td>${row.issue}</td>
        <td>${row.return}</td>
        <td class="${row.status === 'Issued' ? 'status-issued' : 'status-returned'}">${row.status}</td>
      `;
      tbody.appendChild(tr);
    }

    if (row.status === "Issued") issued++;
    else returned++;
  });

  document.getElementById("total").innerText = data.length;
  document.getElementById("issued").innerText = issued;
  document.getElementById("returned").innerText = returned;
}

searchInput.addEventListener("input", e => {
  renderTable(e.target.value.toLowerCase());
});

renderTable();
