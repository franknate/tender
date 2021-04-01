<template>
  <div>
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
    <b-alert
      v-model="showUploadError"
      class="mt-3"
      variant="danger"
      fade
    >
      <b>Upload Falied!</b> {{ uploadError }}
    </b-alert>
  </div>
</template>

<script>
export default {
  data() {
    return {
      roundFile: null,
      uploadError: null,
      showUploadError: false,
    }
  },
  methods: {
    uploadForm() {
      if (this.checkFile) {
        const formData = new FormData();
        formData.append("round_file", this.roundFile);
        formData.append("tender_id", this.currentTender.id)
        formData.append("bid_round", this.currentRound);

        fetch(this.$store.state.BASE_URL + "tenders/" + this.currentTender.id + "/", {
          method: "PUT",
          body: formData,
          headers: {
          "Authorization": "Token " + this.$store.getters.Token
          }
        })
        .then(response => response.json().then(data => ({status: response.status, body: data})))
        .then(response => {
          if (response.status == "202") {
            this.uploadError = null
            this.showUploadError = false
            this.$store.dispatch("reloadTender")
          } else {
            this.uploadError = response.body.message
            this.showUploadError = true
          }
        });
      }
    }
  },
  computed: {
    currentTender() {
      return this.$store.getters.CurrentTender;
    },
    currentRound() {
      return this.currentTender.current_bid_round;
    },
    checkFile() {
      return this.roundFile == null ? null : this.roundFile["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
  }
}
</script>

<style>

</style>