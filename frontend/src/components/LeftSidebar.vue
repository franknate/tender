<template>
  <div>
    <b-button pill variant="outline-secondary" v-b-toggle.sidebar-left id="left-button">
      <b-icon icon="cloud-upload-fill"></b-icon>
    </b-button>
    <b-sidebar id="sidebar-left"  no-header>
      <div class="px-3 py-2">
        <TabsBox />
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import TabsBox from "./TabsBox.vue"

export default {
  components: {
    TabsBox
  }
}
</script>

<style scoped>
#left-button {
  position: fixed;
  bottom: 50%;
  left: 1%;
}
</style>