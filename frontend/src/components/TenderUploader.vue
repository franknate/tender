<template>
  <div>
    <b-form
      id="upload-form"
      @submit.stop.prevent="uploadForm"
    >
      <b-form-group>
        <b-form-file
          v-model="tenderFile"
          placeholder="Choose a file..."
          drop-placeholder="Drop file here..."
          accept=".xlsx"
          :state="checkFile"
          required
        ></b-form-file>
        <b-form-invalid-feedback :state="checkFile">
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      tenderFile: null,
      fileError: "",
      market: null,
      direction: null,
      tender_round: null,
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
    uploadForm() {
      if (this.checkFile) {
        const formData = new FormData();
        formData.append("file", this.tenderFile);
        formData.append("market", this.market);
        formData.append("direction", this.direction);
        formData.append("tender_round", this.tender_round);
        formData.append("bid_round", "1");

        fetch(this.$store.BASE_URL + "tenders/", {
          method: "POST",
          body: formData,
          headers: {
            "Authorization": "Token " + this.$store.getters.Token
          }
        })
        .then(response => response.json())
        .then(result => {
          console.log(result)
        });
      }
    }
  },
  computed: {
    checkFile() {
      return this.tenderFile == null ? null : this.tenderFile["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
  }
};
</script>

<style></style>
