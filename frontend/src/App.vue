<template>
  <div id="app">
    <AppHeader />
    <transition name="fade" mode="out-in">
      <div v-if="this.$store.getters.isAuthenticated" id="main">
        <CenterBox />
        <LeftSidebar />    
        <RightSidebar />
      </div>
      <LoggedOut v-else />
    </transition>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import CenterBox from "./components/CenterBox.vue";
import LeftSidebar from "./components/LeftSidebar.vue";
import RightSidebar from "./components/RightSidebar.vue";
import LoggedOut from "./components/LoggedOut.vue"

export default {
  components: {
    AppHeader,
    CenterBox,
    LeftSidebar,
    RightSidebar,
    LoggedOut
  }
};
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
