<template>
  <div align="center" class="mt-5">
    <h2>Login</h2>
    <p v-if="$route.query.redirect">
      You need to login first.
    </p>
    <form @submit.prevent="login">
      <label><input v-model="user" placeholder="username"></label> <br>
      <label><input v-model="pass" placeholder="password" type="password"></label><br>
      <button type="submit">login</button>
      <p v-if="error" class="error">Bad login information</p>
    </form>
  </div>
</template>

<script>
import auth from '../utils/auth'

export default {
  data () {
    return {
      user: '',
      pass: '',
      error: false
    }
  },
  methods: {
    login () {
      auth.login(this.user, this.pass, loggedIn => {
        if (!loggedIn) {
          this.error = true
        } else {
          this.$router.replace(this.$route.query.redirect || '/batches')
        }
      })
    }
  }
}
</script>

<style>
.error {
  color: red;
}
</style>
