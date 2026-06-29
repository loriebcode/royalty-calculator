// script.js
// Handles the "+ Add another writer/publisher" buttons by cloning
// a new contributor row into the form. Pure vanilla JS, no dependencies.

document.querySelectorAll(".add-row").forEach((button) => {
    button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        const nameField = button.getAttribute("data-name");
        const pctField = button.getAttribute("data-pct");
        const list = document.getElementById(targetId);

        const row = document.createElement("div");
        row.className = "contributor-row";
        row.innerHTML = `
            <input type="text" name="${nameField}" placeholder="Name" required>
            <div class="pct-input">
                <input type="number" step="0.01" min="0" max="100" name="${pctField}" placeholder="%" required>
                <span>%</span>
            </div>
        `;
        list.appendChild(row);

        // Focus the new name field so typing can continue immediately
        row.querySelector('input[type="text"]').focus();
    });
});
