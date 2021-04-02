<template>
  <div>
    <b-form
      id="upload-form"
      @submit.stop.prevent="uploadForm"
    >
      <b-form-group>
        <b-form-file
          v-model="bidFile"
          placeholder="Bid file..."
          drop-placeholder="Bid file..."
          accept=".xlsx"
          :state="checkFile(bidFile)"
          required
        ></b-form-file>
        <b-form-invalid-feedback :state="checkFile(bidFile)">
          Must be an XLSX file
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group>
        <b-form-file
          v-model="dropsFile"
          placeholder="Price drops file..."
          drop-placeholder="Price drops file..."
          accept=".xlsx"
          :state="checkFile(dropsFile)"
          required
        ></b-form-file>
        <b-form-invalid-feedback :state="checkFile(dropsFile)">
          Must be an XLSX file
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group>
        <b-button type="submit" variant="success">Upload</b-button>
      </b-form-group>
    </b-form>
    <b-alert
      v-model="showUploadError"
      variant="danger"
      fade
    >
      <b>Upload Falied!</b> {{ uploadError }}
    </b-alert>
    <b-alert
      v-model="showUploadSuccess"
      variant="success"
      dismissible
      fade
    >
      <b>Uploaded successfully!</b>
    </b-alert>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dropsFile: null,
      bidFile: null,
      uploadError: null,
      showUploadError: false,
      showUploadSuccess: false,
    };
  },
  methods: {
    checkFile(file) {
      return file == null ? null : file["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    },
    uploadForm() {
      if (this.checkFile) {
        const formData = new FormData();
        formData.append("drops_file", this.dropsFile);
        formData.append("bid_file", this.bidFile);

        fetch(this.$store.state.BASE_URL + "tenders/", {
          method: "POST",
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
            this.showUploadSuccess = true
            this.dropsFile = null
            this.bidFile = null
            this.$store.dispatch("getTenders")
          } else {
            this.uploadError = response.body.message
            this.showUploadSuccess = false
            this.showUploadError = true
          }
        });
      }
    }
  }
};
</script>

<style></style>
