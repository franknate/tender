<template>
  <div id="app">
    <AppHeader />
    <b-container class="bv-example-row">
      <b-row>
        <b-col>
          <CenterBox />
        </b-col>
      </b-row>
    </b-container>
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
