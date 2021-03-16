<template>
  <div>
    <b-form
      id="upload-form"
      @submit.stop.prevent="uploadForm"
    >
      <b-form-group>
        <b-form-file
          v-model="tenderFile"
          placeholder="First round file..."
          drop-placeholder="First round file..."
          accept=".xlsx"
          :state="checkFile(tenderFile)"
          required
        ></b-form-file>
        <b-form-invalid-feedback :state="checkFile(tenderFile)">
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
        <b-form-select v-model="market" :options="markets" required></b-form-select>
      </b-form-group>
      <b-form-group>
        <b-form-select v-model="direction" :options="directions" required></b-form-select>
      </b-form-group>
      <b-form-group>
        <b-form-select v-model="tender_round" :options="tender_rounds" required></b-form-select>
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
      tenderFile: null,
      dropsFile: null,
      bidFile: null,
      market: null,
      direction: null,
      tender_round: null,
      uploadError: null,
      showUploadError: false,
      showUploadSuccess: false,
      markets: [
        { value: null, text: "Market" },
        { value: "aFRR", text: "aFRR" },
        { value: "mFRR", text: "mFRR" },
      ],
      directions: [
        { value: null, text: "Direction" },
        { value: "U", text: "Up" },
        { value: "D", text: "Down" },
      ],
      tender_rounds: [
        { value: null, text: "Tender round" },
        { value: 1, text: "1" },
        { value: 2, text: "2" },
      ],
    };
  },
  methods: {
    checkFile(file) {
      return file == null ? null : file["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    },
    clearForm() {
      this.tenderFile = null,
      this.dropsFile = null,
      this.bidFile = null,
      this.market = null,
      this.direction = null,
      this.tender_round = null
    },
    uploadForm() {
      if (this.checkFile) {
        const formData = new FormData();
        formData.append("first_round_file", this.tenderFile);
        formData.append("drops_file", this.dropsFile);
        formData.append("bid_file", this.bidFile);
        formData.append("market", this.market);
        formData.append("direction", this.direction);
        formData.append("tender_round", this.tender_round);
        formData.append("bid_round", "1");

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
            this.clearForm()
            this.$store.commit("getTenders")
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
