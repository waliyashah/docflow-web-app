// JavaScript to toggle Read More / Read Less button for long text
  document.addEventListener('DOMContentLoaded', function() {
    const readMoreButtons = document.querySelectorAll('.read-more-btn');

    readMoreButtons.forEach(function(btn) {
      btn.addEventListener('click', function() {
        const parentTd = btn.parentElement;
        const dots = parentTd.querySelector('.dots');
        const remainingText = parentTd.querySelector('.remaining-text');

        if (remainingText.style.display === 'none') {
          // Expand to show full text
          remainingText.style.display = 'inline';
          dots.style.display = 'none';
          btn.textContent = 'Read Less';
        } else {
          // Collapse back to short text
          remainingText.style.display = 'none';
          dots.style.display = 'inline';
          btn.textContent = 'Read More';
        }
      });
    });
  });

  //Javascript for toggle functionality, Javascript for toggle functionality and handling checkboxes for filters-->
  
  function toggleFilter() {
      var filterSection = document.getElementById("filterSection");
      filterSection.style.display = filterSection.style.display === "none" ? "block" : "none";
  }

// ✅ Ensure DataTables initializes **after jQuery & DataTables scripts are loaded**
$(document).ready(function() {
  // Check if the table exists before initializing DataTables
  if ($('#initiativesTable').length) {
      $('#initiativesTable').DataTable({
          "paging": true,
          "searching": true,
          "ordering": true,
          "info": true,
          "lengthMenu": [5, 10, 25, 50, 100],
          "columnDefs": [
              { "orderable": false, "targets": [3, 4,5 , 6, 7,11] }
          ],
          "responsive": true,
          // ✅ Hide "Show" and Replace with Custom Text
          "language": {

            "lengthMenu": "_MENU_ entries",
        

          // ✅ Custom Pagination Text
          
            "lengthMenu": "_MENU_ entries",
            "info": "Showing _START_ to _END_ of _TOTAL_ Initiatives",
            "paginate": {
                "previous": "«",  // Left Arrow
                "next": "»"       // Right Arrow
            }
        },

        // ✅ Show only limited page numbers
        "pagingType": "simple_numbers"
      });
  }
});



// delete initiatives
$(document).ready(function () {
  console.log("✅ Scripts.js is loaded and running!");

  // Attach event listener to delete button
  $(document).on("click", ".delete-btn", function () {
      let initiativeId = $(this).data("id");
      console.log("🗑️ Delete button clicked! Initiative ID:", initiativeId);

       // Check role from hidden input
       const userRole = $("#user-role").val();
       if (!['Manager', 'Approver'].includes(userRole)) {
           window.location.href = "/unauthorized";
           return;
       }

      if (initiativeId) {
          $("#deleteModal").modal("show");  // Show modal
          $("#confirmDelete").data("id", initiativeId); // Store ID in confirm button
      }
  });

  // When Confirm Delete button is clicked
  $("#confirmDelete").click(function () {
      let deleteInitiativeId = $(this).data("id");
      console.log("🚨 Confirm Delete clicked! Deleting:", deleteInitiativeId);

      if (deleteInitiativeId) {
          // Find row with matching initiative ID and remove it
          let row = $(".delete-btn[data-id='" + deleteInitiativeId + "']").closest("tr");
          row.fadeOut(500, function () {
              $(this).remove();  // Remove row from table
          });

          $("#deleteModal").modal("hide");  // Close modal
      }
  });
});

// Function to handle the checkbox filter 
function toggleCheckboxDropdown() {
  const box = document.getElementById("divisionCheckboxes");
  if (box) {
    box.style.display = box.style.display === "block" ? "none" : "block";
  }
}

//  close if clicked outside
document.addEventListener("click", function (e) {
  const dropdown = document.getElementById("divisionCheckboxes");
  const toggle = document.getElementById("divisionDropdownToggle");
  if (dropdown && toggle && !dropdown.contains(e.target) && !toggle.contains(e.target)) {
    dropdown.style.display = "none";
  }
});



// script for approval/rejection
document.addEventListener("DOMContentLoaded", () => {
  // Approve button logic
  document.querySelectorAll('.approve-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const inId = btn.dataset.id;
      fetch(`/approve_initiative/${inId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            alert('Initiative approved!');
            location.reload();
          }
        });
    });
  });

  // Reject button logic
  document.querySelectorAll('.reject-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const inId = btn.dataset.id;
      fetch(`/reject_initiative/${inId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            alert('Initiative rejected!');
            location.reload();
          }
        });
    });
  });
});


// ✅ Add Employee Row Functionality (Aligned + Removable) - New Initiative

function addEmployeeRow() {
  const container =
    document.getElementById("employee-fields") ||
    document.getElementById("new-employee-fields");

  const wrapper = document.createElement("div");
  wrapper.className = "grid grid-cols-[1fr_1fr_1fr_auto] gap-3 items-center employee-group mt-2";

  wrapper.innerHTML = `
    <input list="emp_ids" name="emp_id" placeholder="Employee ID"
           class="border px-3 py-2 rounded-md text-purple-900" oninput="fillEmpName(this)">
    <input list="emp_names" name="emp_name" placeholder="Employee Name"
           class="border px-3 py-2 rounded-md text-purple-900" oninput="fillEmpID(this)">
    <input list="emp_roles" name="emp_role" placeholder="Employee Role"
           class="border px-3 py-2 rounded-md text-purple-900">
     <button type="button"
            class="remove-emp bg-red-500 text-white w-9 h-9 flex items-center justify-center rounded-md hover:bg-red-600"
            title="Remove Employee"
            onclick="removeEmployeeRow(this)">
        <i class="fas fa-times text-base"></i>
    </button>
    <input type="hidden" name="remove_emp" value="0" />
  `;

  container.appendChild(wrapper);

}  

  function removeEmployeeRow(button) {
    const row = button.closest('.employee-group');
    row.style.display = 'none';
    const hidden = row.querySelector('input[name="remove_emp"]');
    if (hidden) hidden.value = "1";
  }

// ✅ Fill Employee Name based on ID and vice versa
function fillEmpName(input) {
  const id = input.value;
  const row = input.closest('.employee-group');
  const nameInput = row.querySelector('[name="emp_name"]');
  const match = window.employee_records?.find(emp => emp[0] === id);
  if (match) nameInput.value = match[1];
}

function fillEmpID(input) {
  const name = input.value;
  const row = input.closest('.employee-group');
  const idInput = row.querySelector('[name="emp_id"]');
  const match = window.employee_records?.find(emp => emp[1] === name);
  if (match) idInput.value = match[0];
}


