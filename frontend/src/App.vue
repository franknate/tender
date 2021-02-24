<template>
  <div id="app">
    <AppHeader />
    <b-container class="bv-example-row">
      <b-row>
        <b-col>
          <TabsBox />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import TabsBox from "./components/TabsBox.vue";

export default {
  components: {
    AppHeader,
    TabsBox
  }
};
</script>

<style></style>
