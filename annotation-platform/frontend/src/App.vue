<template>
  <div id="app">
    <b-container class="bv-example-row" id="nav" fluid>
      <b-row>
        <b-col>
          <router-link to="/stages">
            <img
              style="height: 40%; object-fit: contain"
              alt="Vue logo"
              src="./assets/logo.png"
            />
          </router-link>
        </b-col>
        <b-col align="center" v-if="isAnnotations"></b-col>
        <b-col align="right" align-v="center">
          <router-link v-if="!loggedIn" to="/">Log in</router-link>
          <router-link v-if="loggedIn" to="/logout">Log out</router-link>
        </b-col>
      </b-row>
    </b-container>
    <router-view />
  </div>
</template>


<script>
import auth from "./utils/auth";

export default {
  data() {
    return {
      loggedIn: auth.loggedIn(),
    };
  },
  created() {
    auth.onChange = (loggedIn) => {
      this.loggedIn = loggedIn;
    };
  },
  computed: {
    isAnnotations() {
      return this.$route.name === 'annotations'
    }
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
