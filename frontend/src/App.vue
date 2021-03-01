<template>
  <div id="app">
    <AppHeader />
    <CenterBox />
    <LeftSidebar />    
    <RightSidebar />
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import CenterBox from "./components/CenterBox.vue";
import LeftSidebar from "./components/LeftSidebar.vue";
import RightSidebar from "./components/RightSidebar.vue";

export default {
  components: {
    AppHeader,
    CenterBox,
    LeftSidebar,
    RightSidebar
  }
};
</script>

<style></style>
