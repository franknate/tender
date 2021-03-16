<template>
  <b-form
    id="upload-form"
    @submit.stop.prevent="uploadForm"
  >
    <b-form-group>
      <b-form-file
        v-model="roundFile"
        placeholder="Next round..."
        drop-placeholder="Drop here..."
        accept=".xlsx"
        :state="checkFile"
        required
      >
      </b-form-file>
      <b-form-invalid-feedback :state="checkFile">
        Must be an XLSX file
      </b-form-invalid-feedback>
    </b-form-group>
    <b-button type="submit" variant="success">Upload</b-button>
  </b-form>
</template>

<script>
export default {
  props: {
    lastRound: Number
  },
  data() {
    return {
      roundFile: null
    }
  },
  methods: {
    uploadForm() {
      if (this.checkFile) {
        const formData = new FormData();
        formData.append("round_file", this.roundFile);
        formData.append("tender_id", this.currentTender.id)
        formData.append("bid_round", this.lastRound + 1);

        fetch(this.$store.state.BASE_URL + "tenders/" + this.currentTender.id + "/", {
          method: "PUT",
          body: formData,
          headers: {
          "Authorization": "Token " + this.$store.getters.Token
          }
        })
        .then(response => response.json())
        .then(result => {
          this.$store.dispatch("reloadTender")
        });
      }
    }
  },
  computed: {
    currentTender() {
      return this.$store.state.currentTender;
    },
    checkFile() {
      return this.roundFile == null ? null : this.roundFile["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
  }
}
</script>

<style>

</style>