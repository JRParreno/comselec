var animation = bodymovin.loadAnimation({
  container: document.getElementById('list-animation'), // Required
  path: '/static/election/json/13861-create-admin.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Hello World", // Name for future reference. Optional.
})

var second = bodymovin.loadAnimation({
  container: document.getElementById('gear-animation'), // Required
  path: '/static/election/json/20932-laptop-with-gear-animation.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Hello World", // Name for future reference. Optional.
})

