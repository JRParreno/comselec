var animation = bodymovin.loadAnimation({
  container: document.getElementById('lottie'), // Required
  path: '/static/users/json/election_login.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Hello World", // Name for future reference. Optional.
})