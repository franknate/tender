<template>
  <div>
    <b-button pill variant="outline-secondary" v-b-toggle.sidebar-left id="open-button">
      <b-icon icon="folder-fill"></b-icon>
    </b-button>
    <b-sidebar id="sidebar-left" width="400px" no-header>
      <div class="px-4 py-3">
        <TabsBox />
      </div>
      <p class="h3">
        <b-icon icon="arrow-bar-left" v-b-toggle.sidebar-left id="hide-icon"></b-icon>
      </p>
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
#open-button {
  position: fixed;
  bottom: 50%;
  left: 1%;
}

#hide-icon {
  color: grey;
  font-weight: 300;
  position: absolute;
  bottom: 50%;
  right: -1px;
}

#hide-icon:hover {
  color: darkslategrey;
  cursor: pointer;
}
</style>