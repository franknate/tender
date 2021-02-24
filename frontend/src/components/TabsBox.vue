<template>
  <div>
    <b-tabs content-class="mt-3" align="center">
      <b-tab title="Select" active>
        <TenderSelector />
      </b-tab>
      <b-tab title="Upload">
        <TenderUploader />
      </b-tab>
    </b-tabs>
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

<style>

</style>