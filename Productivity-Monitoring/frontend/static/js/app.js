// Show the modal
function showModal() {
    document.getElementById('id01').style.display = 'block';
  }
  
  // Hide the modal
  function hideModal() {
    document.getElementById('id01').style.display = 'none';
  }
  
  // Close the modal when clicking outside of it
  window.onclick = function(event) {
    const modal = document.getElementById('id01');
    if (event.target == modal) {
      hideModal();
    }
  }
  