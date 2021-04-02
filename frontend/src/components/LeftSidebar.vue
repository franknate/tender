<template>
  <div>
    <b-button
      pill variant="outline-secondary"
      v-b-toggle.sidebar-left
      id="open-button"
    >
      <b-icon icon="folder-fill"></b-icon>
    </b-button>
    <b-sidebar
      id="sidebar-left"
      width="400px"
      no-header
      shadow
    >
      <div class="px-4 py-2 overflow-auto">
        <h4 class="my-3">Select a Tender</h4>
        <TenderSelector />
      </div>
      <p class="h3">
        <b-icon icon="arrow-bar-left" v-b-toggle.sidebar-left id="hide-icon"></b-icon>
      </p>
      <template #footer>
        <div class="px-4 py-3 border-top">
          <h4 class="my-3">Upload a Tender</h4>
          <TenderUploader />
        </div>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
import TenderSelector from "./TenderSelector.vue";
import TenderUploader from "./TenderUploader.vue";

export default {
  components: {
    TenderSelector,
    TenderUploader
  }
}
</script>

<style scoped>
#sidebar-left {
  position: absolute !important;
  top: 60px !important;
  background-color: aqua !important;
}

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