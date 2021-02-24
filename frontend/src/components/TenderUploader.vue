<template>
  <b-jumbotron
    header="Upload a Tender"
    header-level="4"
    lead="Some useful text"
  >
    <b-form>
      <b-form-file
        v-model="tenderFile"
        placeholder="Choose a file or drop it here..."
        drop-placeholder="Drop file here..."
        required
      ></b-form-file>
      <b-form-datepicker v-model="date" required></b-form-datepicker>
      <b-form-select v-model="market" :options="markets" required></b-form-select>
      <b-form-select v-model="direction" :options="directions" required></b-form-select>
      <b-form-select v-model="tender_round" :options="rounds" required></b-form-select>
      <b-button type="submit" variant="primary">Upload</b-button>
    </b-form>
  </b-jumbotron>
</template>

<script>
export default {
  data() {
    return {
      tenderFile: [],
      date: null,
      market: null,
      direction: null,
      tender_round: null,
      markets: [
        { value: null, text: "Select market" },
        { value: "aFRR", text: "aFRR" },
        { value: "mFRR", text: "mFRR" },
      ],
      directions: [
        { value: null, text: "Select direction" },
        { value: "U", text: "Up" },
        { value: "D", text: "Down" },
      ],
      rounds: [
        { value: null, text: "Select round" },
        { value: 1, text: "1" },
        { value: 2, text: "2" },
      ],
    };
  },
};
</script>

<style></style>
