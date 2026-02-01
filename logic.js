document.addEventListener('DOMContentLoaded', () => {
  const aiButton = document.getElementById('aiButton');
  if (!aiButton) return;

  aiButton.addEventListener('click', () => {
    alert('If you really expected to talk to a chatbot to simplify a website like this even further, re-evaluate your life choices');
    window.location.href = "/files/haha-you-look-hilarious.jpg"
    });
aiButton.style.display = 'block';
});