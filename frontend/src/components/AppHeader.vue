<template>
  <b-navbar type="dark" variant="dark">
    <b-nav-item disabled>Greenergy <b>Tender</b></b-nav-item>
    <b-navbar-nav class="ml-auto">
      <b-nav-item v-if="isLoggedIn" @click="logout" >Log Out</b-nav-item>
      <b-nav-form v-else @submit.prevent="login">
        <b-form-group class="mr-2">
          <b-form-invalid-feedback :state="checkLogin">
            Invalid username or password
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group>
          <b-form-input
            v-model="username"
            size="sm"
            class="mr-sm-2"
            placeholder="usename">
          </b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input
            v-model="password"
            type="password"
            size="sm"
            class="mr-sm-2"
            placeholder="password">
          </b-form-input>
        </b-form-group>
        <b-form-group>
          <b-button
            size="sm"
            class="my-2 my-sm-0"
            type="submit"
          >Log In</b-button>
        </b-form-group>
      </b-nav-form>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  data() {
    return {
      username: null,
      password: null,
      validLogin: null
    }
  },
  methods: {
    login() {
      const User =  {
        username: this.username,
        password: this.password
      }
      this.$store.dispatch("LogIn", User)
      .then(response => {
        this.validLogin = null
        this.username = null
        this.password = null
      }, error => {
        this.validLogin = false
      })
    },
    logout() {
      this.$store.dispatch("LogOut")
    }
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isAuthenticated;
    },
    checkLogin() {
      return this.validLogin
    }
  }
}
</script>

<style>

</style>