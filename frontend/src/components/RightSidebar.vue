<template>
  <div v-if="this.$store.getters.CurrentTender">
    <b-button pill variant="outline-secondary" v-b-toggle.sidebar-right id="right-button">
        <b-icon icon="pen-fill"></b-icon>
    </b-button>
    <b-sidebar
      id="sidebar-right"
      width="550px"
      bg-variant="dark"
      text-variant="light"
      right
      no-header
      shadow
    >
      <div class="px-4 py-3" id="bidTableWrapper">
        <MakeBid />
      </div>
      <p class="h2">
        <b-icon icon="arrow-bar-right" v-b-toggle.sidebar-right id="hide-icon"></b-icon>
      </p>
    </b-sidebar>
  </div>
</template>

<script>
import MakeBid from "./MakeBid.vue"

export default {
  components: {
    MakeBid
  }
}
</script>

<style scoped>
#right-button {
  position: fixed;
  bottom: 50%;
  right: 1%;
}

#hide-icon {
  color: grey;
  font-weight: 300;
  position: absolute;
  bottom: 50%;
}

#hide-icon:hover {
  color: lightgrey;
  cursor: pointer;
}

#bidTableWrapper {
  height: 98%;
}
</style>