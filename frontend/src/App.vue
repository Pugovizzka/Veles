<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

body {
  font-family: 'Gabarito', sans-serif;
  margin: 0;
  padding: 0;
  background: rgba(58, 60, 65, 1);
  color: rgba(243, 238, 232, 1);
}

* {
  box-sizing: border-box;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Gabarito', sans-serif;
  color: rgba(243, 238, 232, 1);
}

p, span, div {
  color: rgba(243, 238, 232, 1);
}
</style>