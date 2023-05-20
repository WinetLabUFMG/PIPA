function isAuthenticated() {
   fetch('/auth')
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Erro:', error);
  });
}

export { isAuthenticated}