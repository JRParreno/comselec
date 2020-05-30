var animation = bodymovin.loadAnimation({
  container: document.getElementById('lottie'), // Required
  path: '/static/users/json/election_login.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Hello World", // Name for future reference. Optional.
})

var voter = bodymovin.loadAnimation({
  container: document.getElementById('voterAnimation'), // Required
  path: '/static/users/json/22744-vote-fill-in-version.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Hello World", // Name for future reference. Optional.
})