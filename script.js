function shuffleWords() {
  const words = ['Hola', 'mi', 'nombre', 'es', 'John'];
  for (let i = words.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [words[i], words[j]] = [words[j], words[i]];
  }
  return words;
}

function displayWords() {
  const wordContainer = document.querySelector('.word-container'); // Assuming there's a container for the words
  const shuffledWords = shuffleWords();
  
  wordContainer.innerHTML = '';
  shuffledWords.forEach(word => {
    const button = document.createElement('button');
    button.className = 'word-button';
    button.textContent = word;
    wordContainer.appendChild(button);
  });
}

// Call displayWords when the page loads
window.addEventListener('load', displayWords);

// Add this to your existing JavaScript
document.getElementById('shuffle-button').addEventListener('click', displayWords);

function showBackButton() {
  const backButton = document.createElement('button');
  backButton.className = 'back-button';
  backButton.innerHTML = '&larr; Back';
  backButton.addEventListener('click', () => {
    history.back();
  });
  
  // Insert back button at the top of the content
  const container = document.querySelector('.landing-container') || document.body;
  container.insertAdjacentElement('afterbegin', backButton);
}

// Add click handlers to all nav buttons
document.querySelectorAll('.nav-button').forEach(button => {
  button.addEventListener('click', () => {
    // Store current page in history before showing back button
    history.pushState({ page: 'home' }, '');
    showBackButton();
  });
}); 